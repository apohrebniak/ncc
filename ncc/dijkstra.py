import ncc.common as cmn
import ncc.lexer_token as lexertoken
import ncc.rpn_token as rpntoken

STATE_NONE, STATE_IF, STATE_ELSE, STATE_WHILE = range(4)


class DijkstraRPNBuilder:
    def __init__(self, ltokens):
        """tokens from lexer"""
        self.ltokens = ltokens
        """array of RPN-tokens in RPN"""
        self.rpn = []
        self.stack = []
        self.lexeme_function_map = self.build_lexeme_function_map()

        self.next_label_index = 0
        """Current state. If in 'do' block, or if in 'else' block"""
        self.state_stack = []
        self.state_stack.append(STATE_NONE)

        self.io_op_args_count = 0

    def build_lexeme_function_map(self):
        return {
            cmn.LB: self.common_left_open,
            cmn.RB: self.right_bracket,
            cmn.LFB: self.common_left_open,
            cmn.RFB: self.right_figure_bracket,
            cmn.LSB: self.common_left_open,
            cmn.RSB: self.right_square_bracket,
            cmn.WHILE: self.while_op,
            cmn.DO: self.do,
            cmn.IF: self.if_op,
            cmn.QM: self.question_mark,
            cmn.DOTS: self.dots,
            cmn.COMMA: self.comma,
            cmn.NL: self.new_line
        }

    def build_new_rtoken(self, ltoken):
        if ltoken.tag in cmn.RPN_SYMS_MAPPING:
            rtag = cmn.RPN_SYMS_MAPPING[ltoken.tag]
        elif ltoken.tag in cmn.RPN_OPS_MAPPING:
            rtag = cmn.RPN_OPS_MAPPING[ltoken.tag]

        return rpntoken.RPNToken(rtag, ltoken.tag,
                                 cmn.RPN_PRIORITIES[rtag],
                                 ltoken.payload)

    """Common function for token"""

    def common(self, ltoken, append=True):

        rtoken = self.build_new_rtoken(ltoken)

        while len(self.stack) != 0:
            if self.stack[-1].prio >= rtoken.prio:
                self.rpn.append(self.stack.pop())
            else:
                break

        if append:
            self.stack.append(rtoken)

        return rtoken

    """Common function for [, {, ("""

    def common_left_open(self, ltoken):
        self.stack.append(self.build_new_rtoken(ltoken))

    def comma(self, ltoken):
        self.io_op_args_count += 1

    def new_line(self, ltoken):
        self.common(ltoken, append=False)

    def while_op(self, ltoken):
        rtoken = self.common(ltoken, append=False)

        label = self.build_next_label()
        # self.labels_stack.append(label)
        self.rpn.append(label)
        combined_token = rpntoken.RPNCombinedWhileToken(rtoken)
        combined_token.labels.append(label)
        self.stack.append(combined_token)

    def do(self, ltoken):
        self.common(ltoken, append=False)
        # [while m1] in stack

        label = self.build_next_label()
        jump_false_op = rpntoken.RPNJumpOperator(cmn.R_JMPF)

        # self.labels_stack.append(label)
        self.rpn.append(label)
        self.rpn.append(jump_false_op)

        self.stack[-1].labels.append(label)

        self.state_stack.append(STATE_WHILE)

    def if_op(self, ltoken):
        rtoken = self.common(ltoken, append=False)

        combined_token = rpntoken.RPNCombinedIfToken(rtoken)
        self.stack.append(combined_token)  # have '[if]' in stack

    def question_mark(self, ltoken):
        self.common(ltoken, append=False)

        # have '[if]' in stack

        label = self.build_next_label()
        jump_false_op = rpntoken.RPNJumpOperator(cmn.R_JMPF)

        self.labels_stack.append(label)
        self.rpn.append(label)
        self.rpn.append(jump_false_op)
        # self.add_label_to_table(label) #TODO
        self.stack[-1].labels.append(label)  # have [if m1] in stack
        self.state_stack.append(STATE_IF)

    def dots(self, ltoken):
        self.common(ltoken, append=False)

        # have '[if m1]' in stack

        label = self.build_next_label()
        jump_oper = rpntoken.RPNJumpOperator(cmn.R_JMP)

        self.rpn.append(label)
        self.rpn.append(jump_oper)
        self.rpn.append(self.labels_stack.pop())
        # self.add_label_to_table(label) #TODO
        self.stack[-1].labels.append(label)  # have [if m1 m2] in stack
        self.state_stack.append(STATE_ELSE)

    def right_square_bracket(self, ltoken):
        self.common(ltoken, append=False)
        self.stack.pop()

    def right_figure_bracket(self, ltoken):
        self.common(ltoken, append=False)
        self.stack.pop()

        curr_state = self.state_stack[-1]
        if curr_state == STATE_WHILE:
            label_2 = self.stack[-1].labels.pop()
            label_1 = self.stack[-1].labels.pop()
            jmp = rpntoken.RPNJumpOperator(cmn.R_JMP)
            self.rpn.append(label_1)
            self.rpn.append(jmp)
            self.rpn.append(label_2)
            self.stack.pop()
            self.state_stack.pop()
        elif curr_state == STATE_ELSE:
            self.rpn.append(self.stack[-1].labels[-1])
            self.stack.pop()
            self.state_stack.pop()
        elif curr_state == STATE_IF:
            self.state_stack.pop()

    def right_bracket(self, ltoken):
        self.common(ltoken, append=False)
        self.stack.pop()

        # workaroud for io operations.
        if self.stack[-1].rtag in [cmn.R_IN, cmn.R_OUT]:
            self.io_op_args_count += 1
            self.rpn.append(rpntoken.RPNArgsCountToken(self.io_op_args_count))
            self.io_op_args_count = 0

    def build_rpn(self):

        for token in self.ltokens:
            if isinstance(token, lexertoken.Constant):
                # pass token directly to rpn
                self.rpn.append(
                    rpntoken.RPNConstant(token.tag, token.payload, token.index))
            elif isinstance(token, lexertoken.Identity):
                # token is identity
                self.rpn.append(
                    rpntoken.RPNIdentity(token.tag, token.payload, token.index))
            elif token.tag in self.lexeme_function_map:
                self.lexeme_function_map[token.tag](token)
            else:
                self.common(token)

        """"Pop all stuff out from stack"""
        while len(self.stack) != 0:
            self.rpn.append(self.stack.pop())
        return self.rpn

    def build_next_label(self):
        label = rpntoken.RPNLabel(index=self.next_label_index)
        self.next_label_index = self.next_label_index + 1
        return label

    def add_label_to_table(self, label):
        self.labels_stack.append(label)
