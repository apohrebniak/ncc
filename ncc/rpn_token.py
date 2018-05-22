import ncc.common as cmn


class RPNToken:
    def __init__(self, rtag, ltag, prio, lexeme):
        self.rtag = rtag
        self.ltag = ltag
        self.prio = prio
        self.lexeme = lexeme

    def __repr__(self):
        return str(self.lexeme)


class RPNConstant:
    def __init__(self, ltag, lexeme, index):  # TODO: maybe remove index
        self.ltag = ltag
        self.lexeme = lexeme
        self.index = index

    def __repr__(self):
        return str(self.lexeme)


class RPNIdentity:
    def __init__(self, ltag, lexeme, index):  # TODO: maybe remove index
        self.lexeme = lexeme
        self.index = index
        self.ltag = ltag

    def __repr__(self):
        return str(self.lexeme)


class RPNLabel:
    def __init__(self, index, offset):
        self.index = index
        self.offset = offset

    def __repr__(self):
        return "lbl_" + str(self.index)


class RPNJumpOperator:
    def __init__(self, rtag):
        self.rtag = rtag

    def __repr__(self):
        return "JMPF" if self.rtag == cmn.R_JMPF else "JMP"


class RPNCombinedIfToken:
    def __init__(self, if_token):
        self.if_token = if_token
        self.prio = if_token.prio
        self.labels = []

    def __repr__(self):
        return "[{},{}]".format(repr(self.if_token), repr(self.labels))


class RPNCombinedWhileToken:
    def __init__(self, while_token):
        self.while_token = while_token
        self.prio = while_token.prio
        self.labels = []


class RPNArgsCountToken:
    def __init__(self, count):
        self.count = count

    def __repr__(self):
        return "count_" + str(self.count)
