import sys
from ncc.Token import Token, Word, Constant
from ncc.Table import Table


class Lexer:
    LSB, RSB, LFB, RFB, LB, RB, WHILE, DO, IN, OUT, OR, AND, NOT, \
    INT, FLOAT, IF, DOTS, EQ, PLUS, MINUS, MUL, DIV, NEQ, LOW, LOWEQ, \
    HI, HIEQ, ID, CONST, NL, QM = range(31)

    SYMBOLS = {'[': LSB, ']': RSB, '{': LFB, '}': RFB, '(': LB, ')': RB,
               ':': DOTS, '=': EQ, '+': PLUS, '-': MINUS, '*': MUL, '/': DIV,
               '!=': NEQ, '<': LOW, '<=': LOWEQ, '>': HI, '>=': HIEQ, '\n': NL, '?': QM}

    WORDS = {"if": IF, "while": WHILE, "do": DO, "in": IN, "out": OUT, "or": OR,
             "and": AND, "not": NOT, "int": INT, "float": FLOAT}

    TYPES = {"int", "float"}

    def __init__(self, src):
        self.src = src
        self.strBuffer = ''
        self.lineNum = 1
        self.charNum = 0
        self.sym = ''
        self.readNext = True
        self.tokens = []
        self.ids = Table(3)
        self.constants = Table(2)
        self.typeBuffer = None

    def add_token(self):
        print(self.strBuffer)

        if self.strBuffer in self.SYMBOLS:
            self.tokens.append(Token(self.SYMBOLS[self.strBuffer]))
        elif self.strBuffer in self.WORDS:
            self.tokens.append(Word(self.WORDS[self.strBuffer], self.strBuffer, 0))
        else:

            value = self.strBuffer
            row = self.ids.get_row_for_value(value, 0)

            if row is None:
                index = self.ids.add_row(value, self.constants.next_index(), "unknown")
            else:
                index = self.ids.next_index()

            self.tokens.append(Constant(self.CONST, value, index))

        self.strBuffer = ""

    def add_constant_token(self):

        value = float(self.strBuffer)
        row = self.constants.get_row_for_value(value, 0)

        if row is None:
            index = self.constants.add_row(value, self.constants.next_index())
        else:
            index = self.constants.next_index()

        self.tokens.append(Constant(self.CONST, value, index))

        self.strBuffer = ""

    def add_to_buffer(self):
        self.strBuffer = self.strBuffer + self.sym

    def error(self):
        print("Lexer error! at", self.lineNum, ":", self.charNum)
        sys.exit(1)

    def read_next_symbol(self):
        if self.readNext:
            self.sym = self.src.read(1)

            if self.sym == '\n':
                self.lineNum = self.lineNum + 1
                self.charNum = 0
            else:
                self.charNum = self.charNum + 1

        self.readNext = True

        return self.sym

    def scan(self):
        while True:
            self.read_next_symbol()

            while self.sym in [' ', '\t']:
                self.read_next_symbol()

            self.add_to_buffer()

            if len(self.sym) == 0:
                return

            if self.sym.isalpha():
                self.state_2()
            elif self.sym.isdigit():
                self.state_3()
            elif self.sym == '.':
                self.state_4()
            elif self.sym == '!':
                self.state_5()
            elif self.sym == '=':
                self.state_6()
            elif self.sym == '<':
                self.state_7()
            elif self.sym == '>':
                self.state_8()
            elif self.sym in [',', '\n', '+', '-', '*', '/', '(', ')', '[', ']', '{', '}', '?', ':']:
                self.state_9()
            else:
                self.error()

    def state_2(self):
        self.read_next_symbol()

        if self.sym.isalpha() or self.sym.isdigit():
            self.add_to_buffer()
            self.state_2()
        else:
            self.readNext = False
            self.add_token()

    def state_3(self):
        self.read_next_symbol()

        if self.sym.isdigit():
            self.add_to_buffer()
            self.state_3()
        elif self.sym == '.':
            self.add_to_buffer()
            self.state_4()
        else:
            self.readNext = False
            self.add_constant_token()

    def state_4(self):
        self.read_next_symbol()

        if self.sym.isdigit():
            self.add_to_buffer()
            self.state_10()
        else:
            self.error()

    def state_5(self):
        self.read_next_symbol()

        if self.sym == '=':
            self.add_to_buffer()
            self.add_token()
        else:
            self.error()

    def state_6(self):
        self.read_next_symbol()

        if self.sym == '=':
            self.add_to_buffer()
            self.add_token()
        else:
            self.add_token()
            self.readNext = False

    def state_7(self):
        self.read_next_symbol()

        if self.sym == '=':
            self.add_to_buffer()
            self.add_token()
        else:
            self.add_token()
            self.readNext = False

    def state_8(self):
        self.read_next_symbol()

        if self.sym == '=':
            self.add_to_buffer()
            self.add_token()
        else:
            self.add_token()
            self.readNext = False

    def state_9(self):
        self.add_token()

    def state_10(self):

        """exception state for constants"""

        self.read_next_symbol()

        if self.sym.isdigit():
            self.add_to_buffer()
            self.state_3()
        else:
            self.readNext = False
            self.add_token()
