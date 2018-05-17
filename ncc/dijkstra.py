import ncc.common as cmn
import ncc.lexer_token as lexertoken
import ncc.rpn_token as rpntoken


class DijkstraRPNBuilder:
    def __init__(self, ltokens):
        """tokens from lexer"""
        self.ltokens = ltokens
        """array of RPN-tokens in RPN"""
        self.rpn = []
        self.stack = []
        self.lexeme_function_map = self.build_lexeme_function_map()

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
            cmn.LSB: self.foo,
            cmn.RSB: self.foo,
            cmn.WHILE: self.foo,
            cmn.DO: self.foo,
            cmn.IN: self.foo,
            cmn.OUT: self.foo,
            cmn.OR: self.foo,
            cmn.AND: self.foo,
            cmn.NOT: self.foo,
            cmn.IF: self.foo,
            cmn.DOTS: self.foo,
            cmn.EQ: self.foo,
            cmn.NEQ: self.foo,
            cmn.LOW: self.foo,
            cmn.LOWEQ: self.foo,
            cmn.HI: self.foo,
            cmn.HIEQ: self.foo,
            cmn.QM: self.foo,
            cmn.COMMA: self.foo,
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

    def foo(self, ltoken):
        pass

    # def float_type(self, ltoken):
    #     rtoken = rpntoken.RPNToken(cmn.R_FLOAT, cmn.FLOAT,
    #                                cmn.RPN_PRIORITIES[cmn.R_FLOAT],
    #                                ltoken.payload)
    #     while len(self.stack) != 0:
    #         if self.stack[-1].prio >= rtoken.prio:
    #             self.rpn.append(self.stack.pop())
    #         else:
    #             break
    #     self.stack.append(rtoken)
    #
    # def int_type(self, ltoken):
    #     rtoken = rpntoken.RPNToken(cmn.R_INT, cmn.INT,
    #                                cmn.RPN_PRIORITIES[cmn.R_INT],
    #                                ltoken.payload)
    #     while len(self.stack) != 0:
    #         if self.stack[-1].prio >= rtoken.prio:
    #             self.rpn.append(self.stack.pop())
    #         else:
    #             break
    #     self.stack.append(rtoken)
    #
    # def assign(self, ltoken):
    #     rtoken = rpntoken.RPNToken(cmn.R_ASSGN, cmn.ASSIGN,
    #                                cmn.RPN_PRIORITIES[cmn.R_ASSGN],
    #                                ltoken.payload)
    #     while len(self.stack) != 0:
    #         if self.stack[-1].prio >= rtoken.prio:
    #             self.rpn.append(self.stack.pop())
    #         else:
    #             break
    #     self.stack.append(rtoken)

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

    # def plus(self, ltoken):
    #     rtoken = rpntoken.RPNToken(cmn.R_PLUS, cmn.PLUS,
    #                                cmn.RPN_PRIORITIES[cmn.R_PLUS],
    #                                ltoken.payload)
    #     while len(self.stack) != 0:
    #         if self.stack[-1].prio >= rtoken.prio:
    #             self.rpn.append(self.stack.pop())
    #         else:
    #             break
    #     self.stack.append(rtoken)
    #
    # def minus(self, ltoken):
    #     rtoken = rpntoken.RPNToken(cmn.R_MINUS, cmn.MINUS,
    #                                cmn.RPN_PRIORITIES[cmn.R_MINUS],
    #                                ltoken.payload)
    #     while len(self.stack) != 0:
    #         if self.stack[-1].prio >= rtoken.prio:
    #             self.rpn.append(self.stack.pop())
    #         else:
    #             break
    #     self.stack.append(rtoken)
    #
    # def multiply(self, ltoken):
    #     rtoken = rpntoken.RPNToken(cmn.R_MUL, cmn.MUL,
    #                                cmn.RPN_PRIORITIES[cmn.R_MUL],
    #                                ltoken.payload)
    #     while len(self.stack) != 0:
    #         if self.stack[-1].prio >= rtoken.prio:
    #             self.rpn.append(self.stack.pop())
    #         else:
    #             break
    #     self.stack.append(rtoken)
    #
    # def division(self, ltoken):
    #     rtoken = rpntoken.RPNToken(cmn.R_DIV, cmn.DIV,
    #                                cmn.RPN_PRIORITIES[cmn.R_DIV],
    #                                ltoken.payload)
    #     while len(self.stack) != 0:
    #         if self.stack[-1].prio >= rtoken.prio:
    #             self.rpn.append(self.stack.pop())
    #         else:
    #             break
    #     self.stack.append(rtoken)

    def build_rpn(self):

        for token in self.ltokens:
            if token.tag == cmn.NL:
                continue  # skip
            elif isinstance(token, lexertoken.Constant):
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
