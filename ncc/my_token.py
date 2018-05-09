class Token:
    def __init__(self, tag, row_num, column_num, lexeme):
        self.tag = tag
        self.row_num = row_num
        self.column_num = column_num
        self.payload = lexeme


class Word(Token):
    def __init__(self, tag, row_num, column_num, lexeme, index):
        super().__init__(tag, row_num, column_num, lexeme)
        self.index = index


class Constant(Token):
    def __init__(self, tag, row_num, column_num, value, index):
        super().__init__(tag, row_num, column_num, value)
        self.index = index
