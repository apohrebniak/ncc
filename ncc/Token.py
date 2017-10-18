class Token:

    def __init__(self, tag):
        self.tag = tag


class Word(Token):

    def __init__(self, tag, lexeme, index):
        super().__init__(tag)
        self.lexeme = lexeme
        self.index = index


class Constant(Token):

    def __init__(self, tag, value, index):
        super().__init__(tag)
        self.value = value
        self.index = index