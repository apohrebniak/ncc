class Tocken:
    def __init__(self, tag):
        self.tag = tag


class Word(Tocken):

    def __init__(self, tag, lexeme, index):
        super().__init__(tag)
        self.lexeme = lexeme
        self.index = index


class Constant(Tocken):

    def __init__(self, tag, value, index):
        super().__init__(tag)
        self.value = value
        self.index = index