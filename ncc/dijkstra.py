import ncc.common as cmn
import ncc.lexer_token as lexertoken
import ncc.rpn_token as rpntoken

NONE, STATE_IF, STATE_ELSE, STATE_WHILE, STATE_IO_OP = range(
    5)  # TODO: maybe add state for ) in case of in/out ops


class DijkstraRPNBuilder:
    def __init__(self, ltokens):
        """tokens from lexer"""
        self.ltokens = ltokens
        """array of RPN-tokens in RPN"""
        self.rpn = []
        self.stack = []
        self.lexeme_function_map = self.build_lexeme_function_map()

        self.next_label_index = 0
        self.labels_stack = []  # TODO: use this tack or remove list in Combined token

        self.state = NONE
        self.io_op_args_count = 0

    def build_lexeme_function_map(self):
        return {
            cmn.LB: self.left_bracket,
            cmn.RB: self.right_bracket,
            cmn.PLUS: self.common,
            cmn.MINUS: self.common,
            cmn.MUL: self.common,
            cmn.DIV: self.common,
            cmn.LFB: self.left_figure_bracket,
            cmn.RFB: self.right_figure_bracket,
            cmn.INT: self.common,
            cmn.FLOAT: self.common,
            cmn.ASSIGN: self.common,
            cmn.LSB: self.left_square_bracket,
            cmn.RSB: self.right_square_bracket,
            cmn.WHILE: self.while_op,
            cmn.DO: self.do,
            cmn.IN: self.common,
            cmn.OUT: self.common,
            cmn.OR: self.common,
            cmn.AND: self.common,
            cmn.NOT: self.common,
            cmn.IF: self.if_op,
            cmn.QM: self.question_mark,
            cmn.DOTS: self.dots,
            cmn.EQ: self.common,
            cmn.NEQ: self.common,
            cmn.LOW: self.common,
            cmn.LOWEQ: self.common,
            cmn.HI: self.common,
            cmn.HIEQ: self.common,
            cmn.COMMA: self.comma,
            cmn.NL: self.new_line,
            cmn.UNARY_MINUS: self.common
        }

    """Common function for token"""

    def common(self, ltoken):
        if ltoken.payload in cmn.RPN_SYMBOLS:
            rtag = cmn.RPN_SYMBOLS[ltoken.payload]
        elif ltoken.payload in cmn.RPN_OPERATORS:
            rtag = cmn.RPN_OPERATORS[ltoken.payload]

        rtoken = rpntoken.RPNToken(rtag, ltoken.tag,
                                   cmn.RPN_PRIORITIES[rtag],
                                   ltoken.payload)

        while len(self.stack) != 0:
            if self.stack[-1].prio >= rtoken.prio:
                self.rpn.append(self.stack.pop())
            else:
                break
        self.stack.append(rtoken)

    def comma(self, ltoken):
        self.io_op_args_count += 1

    def new_line(self, ltoken):
        rtoken = rpntoken.RPNToken(cmn.R_NL, ltoken.tag,
                                   cmn.RPN_PRIORITIES[cmn.R_NL],
                                   ltoken.payload)

        while len(self.stack) != 0:
            if self.stack[-1].prio >= rtoken.prio:
                self.rpn.append(self.stack.pop())
            else:
                break

    def while_op(self, ltoken):
        rtoken = rpntoken.RPNToken(cmn.R_WHILE, ltoken.tag,
                                   cmn.RPN_PRIORITIES[cmn.R_WHILE],
                                   ltoken.payload)

        while len(self.stack) != 0:
            if self.stack[-1].prio >= rtoken.prio:
                self.rpn.append(self.stack.pop())
            else:
                break

        label = self.build_next_label()
        # self.labels_stack.append(label)
        self.rpn.append(label)
        combined_token = rpntoken.RPNCombinedWhileToken(rtoken)
        combined_token.labels.append(label)
        self.stack.append(combined_token)

    def do(self, ltoken):
        rtoken = rpntoken.RPNToken(cmn.R_DO, ltoken.tag,
                                   cmn.RPN_PRIORITIES[cmn.R_DO],
                                   ltoken.payload)

        while len(self.stack) != 0:
            if self.stack[-1].prio >= rtoken.prio:
                self.rpn.append(self.stack.pop())
            else:
                break
        # [while m1] in stack

        label = self.build_next_label()
        jump_false_op = rpntoken.RPNJumpOperator(cmn.R_JMPF)

        # self.labels_stack.append(label)
        self.rpn.append(label)
        self.rpn.append(jump_false_op)

        self.stack[-1].labels.append(label)

    def if_op(self, ltoken):
        rtoken = rpntoken.RPNToken(cmn.R_IF, ltoken.tag,
                                   cmn.RPN_PRIORITIES[cmn.R_IF],
                                   ltoken.payload)

        while len(self.stack) != 0:
            if self.stack[-1].prio >= rtoken.prio:
                self.rpn.append(self.stack.pop())
            else:
                break
        combined_token = rpntoken.RPNCombinedIfToken(rtoken)
        self.stack.append(combined_token)  # have '[if]' in stack

    def question_mark(self, ltoken):
        rtoken = rpntoken.RPNToken(cmn.R_QM, ltoken.tag,
                                   cmn.RPN_PRIORITIES[cmn.R_QM],
                                   ltoken.payload)

        while len(self.stack) != 0:
            if self.stack[-1].prio >= rtoken.prio:
                self.rpn.append(self.stack.pop())
            else:
                break

        # have '[if]' in stack

        label = self.build_next_label()
        jump_false_op = rpntoken.RPNJumpOperator(cmn.R_JMPF)

        self.labels_stack.append(label)
        self.rpn.append(label)
        self.rpn.append(jump_false_op)
        # self.add_label_to_table(label) #TODO
        self.stack[-1].labels.append(label)  # have [if m1] in stack

    def dots(self, ltoken):
        rtoken = rpntoken.RPNToken(cmn.R_DOTS, ltoken.tag,
                                   cmn.RPN_PRIORITIES[cmn.R_DOTS],
                                   ltoken.payload)

        while len(self.stack) != 0:
            if self.stack[-1].prio >= rtoken.prio:
                self.rpn.append(self.stack.pop())
            else:
                break

        # have '[if m1]' in stack

        label = self.build_next_label()
        jump_oper = rpntoken.RPNJumpOperator(cmn.R_JMP)

        self.rpn.append(label)
        self.rpn.append(jump_oper)
        self.rpn.append(self.labels_stack.pop())
        # self.add_label_to_table(label) #TODO
        self.stack[-1].labels.append(label)  # have [if m1 m2] in stack

    def left_square_bracket(self, ltoken):
        self.stack.append(
            rpntoken.RPNToken(cmn.R_LSB, ltoken.tag,
                              cmn.RPN_PRIORITIES[cmn.R_LSB],
                              ltoken.payload))

    def right_square_bracket(self, ltoken):
        rtoken = rpntoken.RPNToken(cmn.R_RSB, ltoken.tag,
                                   cmn.RPN_PRIORITIES[cmn.R_RSB],
                                   ltoken.payload)
        while self.stack[-1].ltag != cmn.LSB:
            if self.stack[-1].prio >= rtoken.prio:
                self.rpn.append(self.stack.pop())
        self.stack.pop()

    def left_figure_bracket(self, ltoken):
        self.stack.append(
            rpntoken.RPNToken(cmn.R_LFB, ltoken.tag,
                              cmn.RPN_PRIORITIES[cmn.R_LFB],
                              ltoken.payload))

    def right_figure_bracket(self, ltoken):
        rtoken = rpntoken.RPNToken(cmn.R_RFB, ltoken.tag,
                                   cmn.RPN_PRIORITIES[cmn.R_RFB],
                                   ltoken.payload)
        while self.stack[-1].ltag != cmn.LFB:
            if self.stack[-1].prio >= rtoken.prio:
                self.rpn.append(self.stack.pop())
        self.stack.pop()

        # FIXME workaround for whiles. If closing the "do" block, check for labels in stack
        while len(self.stack) != 0 and isinstance(self.stack[-1],
                                                  rpntoken.RPNCombinedWhileToken):
            if len(self.stack[-1].labels) == 2:
                label_2 = self.stack[-1].labels.pop()
                label_1 = self.stack[-1].labels.pop()
                jmp = rpntoken.RPNJumpOperator(cmn.R_JMP)
                self.rpn.append(label_1)
                self.rpn.append(jmp)
                self.rpn.append(label_2)
                self.stack.pop()
            else:
                break

        # FIXME workaround for ifs. If closing the "else" block, check for labels in stack
        while len(self.stack) != 0 and isinstance(self.stack[-1],
                                                  rpntoken.RPNCombinedIfToken):
            if len(self.stack[-1].labels) == 2:
                self.rpn.append(self.stack[-1].labels[-1])
                self.stack.pop()
            else:
                break

    def left_bracket(self, ltoken):
        self.stack.append(
            rpntoken.RPNToken(cmn.R_ALB, ltoken.tag,
                              cmn.RPN_PRIORITIES[cmn.R_ALB],
                              ltoken.payload))

    def right_bracket(self, ltoken):
        rtoken = rpntoken.RPNToken(cmn.R_ARB, ltoken.tag,
                                   cmn.RPN_PRIORITIES[cmn.R_ARB],
                                   ltoken.payload)
        while self.stack[-1].ltag != cmn.LB:
            if self.stack[-1].prio >= rtoken.prio:
                self.rpn.append(self.stack.pop())
        self.stack.pop()

        # FIXME: workaroud for io operations.
        if self.stack[-1].rtag in [cmn.R_IN, cmn.R_OUT]:
            self.io_op_args_count += 1
            self.rpn.append(rpntoken.RPNArgsCountToken(self.io_op_args_count))
            self.io_op_args_count = 0

    def build_rpn(self):

        for token in self.ltokens:
            # if token.tag == cmn.NL:
            # self.common(token)
            if isinstance(token, lexertoken.Constant):
                # pass token directly to rpn
                self.rpn.append(
                    rpntoken.RPNConstant(token.tag, token.payload, token.index))
            elif isinstance(token, lexertoken.Identity):
                # token is identity
                self.rpn.append(
                    rpntoken.RPNIdentity(token.tag, token.payload, token.index))
            else:
                self.lexeme_function_map[token.tag](token)

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


if __name__ == "__main__":
    tokens = [lexertoken.Token(cmn.LFB, 0, 0, '{'),
              # lexertoken.Token(cmn.LB, 0, 0, '('),
              # lexertoken.Constant(cmn.ID, 0, 0, 1, 0),
              # lexertoken.Token(cmn.PLUS, 0, 0, "+"),
              # lexertoken.Constant(cmn.ID, 0, 0, 2, 1),
              # lexertoken.Token(cmn.RB, 0, 0, ")"),
              # lexertoken.Token(cmn.MUL, 0, 0, "*"),
              # lexertoken.Token(cmn.LB, 0, 0, '('),
              # lexertoken.Constant(cmn.ID, 0, 0, 3, 2),
              # lexertoken.Token(cmn.MINUS, 0, 0, "-"),
              # lexertoken.Constant(cmn.ID, 0, 0, 3, 10),
              # lexertoken.Token(cmn.RB, 0, 0, ")"),
              lexertoken.Token(cmn.INT, 0, 0, "int"),
              lexertoken.Identity(cmn.CONST, 0, 0, "a", 0),
              lexertoken.Token(cmn.EQ, 0, 0, "="),
              # lexertoken.Token(cmn.LB, 0, 0, '('),
              lexertoken.Constant(cmn.ID, 0, 0, 1, 0),
              lexertoken.Token(cmn.PLUS, 0, 0, "+"),
              lexertoken.Constant(cmn.ID, 0, 0, 2, 1),
              # lexertoken.Token(cmn.RB, 0, 0, ")"),
              lexertoken.Token(cmn.RFB, 0, 0, "}")]  # {int a = 1 + 2}
    builder = DijkstraRPNBuilder(tokens)
    rpn = builder.build_rpn()
    print(rpn)
