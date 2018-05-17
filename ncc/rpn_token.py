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
        # metka
