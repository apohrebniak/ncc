import sys
from ncc.token import Token, Word, Constant
from ncc.table import Table
from ncc.common import *


class Lexer:
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

    def add_token(self):

        if self.strBuffer in SYMBOLS:
            self.tokens.append(Token(SYMBOLS[self.strBuffer], self.lineNum))
        elif self.strBuffer in WORDS:
            self.tokens.append(Token(WORDS[self.strBuffer], self.lineNum))
        else:

            value = self.strBuffer
            row = self.ids.get_row_for_value(value, 0)

            if row is None:
                if len(self.tokens) > 0 and self.tokens[-1].tag in TYPES:
                    index = self.ids.add_row(value, self.constants.next_index(), TYPES[self.tokens[-1].tag])
                else:
                    self.error("Unknown variable " + self.strBuffer)
            else:
                index = row[1]

            self.tokens.append(Word(ID, self.lineNum, value, index))

        self.strBuffer = ""

    def add_constant_token(self):

        value = float(self.strBuffer) if "." in self.strBuffer else int(self.strBuffer)
        row = self.constants.get_row_for_value(value, 0)

        if row is None:
            index = self.constants.add_row(value, self.constants.next_index())
        else:
            index = self.constants.next_index()

        self.tokens.append(Constant(CONST, self.lineNum, value, index))

        self.strBuffer = ""

    def add_to_buffer(self):
        self.strBuffer = self.strBuffer + self.sym

    def error(self, msg="Lexer error!"):
        print(msg, " at", self.lineNum, ":", self.charNum)
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
