import sys
from ncc.Tocken import Tocken, Word, Constant

class Tocken:

    def __init__(self, index = None, value = None, ):
        pass

class Lexer:
    LSB, RSB, LFB, RFB, LB, RB, WHILE, DO, IN, OUT, OR, AND, NOT, \
    INT, FLOAT, IF, DOTS, EQ, PLUS, MINUS, MUL, DIV, NEQ, LOW, LOWEQ, \
    HI, HIEQ, ID, CONST, NL, QM = range(31)

    SYMBOLS = {'[': LSB, ']': RSB, '{': LFB, '}': RFB, '(': LB, ')': RB,
               ':': DOTS, '=': EQ, '+': PLUS, '-': MINUS, '*': MUL, '/': DIV,
               '!=': NEQ, '<': LOW, '<=': LOWEQ, '>': HI, '>=': HIEQ, '\n': NL, '?': QM}

    WORDS = {"while": WHILE, "do": DO, "in": IN, "out": OUT, "or": OR,
             "and": AND, "not": NOT, "int": INT, "float": FLOAT}

    def __init__(self, src):
        self.src = src
        self.strBuffer = ''
        self.lineNum = 1
        self.charNum = 0
        self.sym = ''
        self.readNext = True
        self.tockens = []
        self.ids = []
        self.constants = []

    def add_tocken(self):
        print(self.strBuffer)

        if self.strBuffer in self.SYMBOLS:
            self.tockens.append(Tocken(self.SYMBOLS[self.strBuffer]))
        elif self.strBuffer in self.WORDS:
            self.tockens.append(Word(self.WORDS[self.strBuffer], self.strBuffer, 0))

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
            self.add_tocken()

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
            self.add_tocken()

    def state_4(self):
        self.read_next_symbol()

        if self.sym.isdigit():
            self.add_to_buffer()
            self.state_3()
        else:
            self.error()

    def state_5(self):
        self.read_next_symbol()

        if self.sym == '=':
            self.add_to_buffer()
            self.add_tocken()
        else:
            self.error()

    def state_6(self):
        self.read_next_symbol()

        if self.sym == '=':
            self.add_to_buffer()
            self.add_tocken()
        else:
            self.add_tocken()
            self.readNext = False

    def state_7(self):
        self.read_next_symbol()

        if self.sym == '=':
            self.add_to_buffer()
            self.add_tocken()
        else:
            self.add_tocken()
            self.readNext = False

    def state_8(self):
        self.read_next_symbol()

        if self.sym == '=':
            self.add_to_buffer()
            self.add_tocken()
        else:
            self.add_tocken()
            self.readNext = False

    def state_9(self):
        self.add_tocken()
