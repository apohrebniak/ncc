import sys

from ncc.common import *
from ncc.my_token import Token, Word, Constant
from ncc.environment import IndTable, ConstantTable


class Lexer:
    def __init__(self, src):
        """source stream"""
        self.src = src
        """lexeme buffer"""
        self.strBuffer = ''
        self.lineNum = 1
        self.charNum = 0
        self.sym = ''
        self.nextSym = None
        self.tokens = []
        self.ids = IndTable()
        self.constants = ConstantTable()

    def add_token(self):

        # if lexeme is grammar symbol or word
        if self.strBuffer in SYMBOLS:
            self.tokens.append(Token(SYMBOLS[self.strBuffer], self.lineNum))
        elif self.strBuffer in WORDS:
            self.tokens.append(Token(WORDS[self.strBuffer], self.lineNum))
        else:
            # else assume lexeme is id
            value = self.strBuffer
            if self.ids.contains_value(value):
                index = self.ids.get_index_of_value(value)
            elif len(self.tokens) > 0 and self.tokens[-1].tag in TYPES:
                index = self.ids.add_and_get_index(value, TYPES[self.tokens[-1].tag])
            else:
                self.error("Unknown variable " + self.strBuffer)

            self.tokens.append(Word(ID, self.lineNum, value, index))

        self.strBuffer = ""

    def add_constant_token(self):

        value = float(self.strBuffer) if "." in self.strBuffer else int(self.strBuffer)
        index = self.constants.get_index_of_value(value) if self.constants.contains_value(value) \
            else self.constants.add_and_get_index(value)

        self.tokens.append(Constant(CONST, self.lineNum, value, index))

        self.strBuffer = ""

    def add_to_buffer(self):
        self.strBuffer = self.strBuffer + self.sym

    def error(self, msg="Lexer error!"):
        print(msg, " at", self.lineNum, ":", self.charNum)
        sys.exit(1)

    def read_next_symbol(self):
        if not self.nextSym:
            self.sym = self.src.read(1)
        else:
            self.sym = self.nextSym
            self.nextSym = None

        if self.sym == '\n':
            self.lineNum = self.lineNum + 1
            self.charNum = 0
        else:
            self.charNum = self.charNum + 1

        return self.sym

    def look_next_symbol(self):
        """just read next symbol """
        self.nextSym = self.src.read(1)
        return self.nextSym

    def scan(self):
        while True:
            self.read_next_symbol()

            # skip whitespaces
            while self.sym in [' ', '\t']:
                self.read_next_symbol()

            self.add_to_buffer()

            # if EOF then exit
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
        """letter"""
        self.look_next_symbol()

        if self.nextSym.isalpha() or self.nextSym.isdigit():
            self.read_next_symbol()
            self.add_to_buffer()
            self.state_2()
        else:
            self.add_token()

    def state_3(self):
        """digit"""
        self.look_next_symbol()

        if self.nextSym.isdigit():
            self.read_next_symbol()
            self.add_to_buffer()
            self.state_3()
        elif self.nextSym == '.':
            self.read_next_symbol()
            self.add_to_buffer()
            self.state_4()
        else:
            self.add_constant_token()

    def state_4(self):
        """decimal dot"""
        self.look_next_symbol()

        if self.nextSym.isdigit():
            self.read_next_symbol()
            self.add_to_buffer()
            self.state_10()
        else:
            self.error()

    def state_5(self):
        """!"""
        self.look_next_symbol()

        if self.nextSym == '=':
            self.read_next_symbol()
            self.add_to_buffer()
            self.add_token()
        else:
            self.error()

    def state_6(self):
        """="""
        self.look_next_symbol()

        if self.nextSym == '=':
            self.read_next_symbol()
            self.add_to_buffer()
            self.add_token()
        else:
            self.add_token()

    def state_7(self):
        """<"""
        self.look_next_symbol()

        if self.nextSym == '=':
            self.read_next_symbol()
            self.add_to_buffer()
            self.add_token()
        else:
            self.add_token()

    def state_8(self):
        """>"""
        self.look_next_symbol()

        if self.nextSym == '=':
            self.read_next_symbol()
            self.add_to_buffer()
            self.add_token()
        else:
            self.add_token()

    def state_9(self):
        """separator"""
        self.add_token()

    def state_10(self):

        """exception state for constants"""

        self.look_next_symbol()

        if self.nextSym.isdigit():
            self.read_next_symbol()
            self.add_to_buffer()
            self.state_3()
        else:
            self.add_constant_token()
