class Token:
    def __init__(self, tag, row_num):
        self.tag = tag
        self.row_num = row_num


class Word(Token):
    def __init__(self, tag, row_num, lexeme, index):
        super().__init__(tag, row_num)
        self.payload = lexeme
        self.index = index


class Constant(Token):
    def __init__(self, tag, row_num, value, index):
        super().__init__(tag, row_num)
        self.payload = value
        self.index = index
