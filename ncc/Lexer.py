import sys


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
        self.buffer = ''
        self.line = 0
        self.char = 0

    def error(self):
        print("Lexer error!")
        sys.exit(1)

    def nextChar(self):
        c = self.src.read(1)
        while c in [' ', '\t']:
            c = self.src.read(1)

        if c == '\n':
            self.line = self.line + 1
            self.char = 0
        else:
            self.char = self.char + 1

        return c

    def scan(self):
        print("state_1")
        while True:
            sym = self.nextChar()
            print('[', sym, ']')

            if len(sym) == 0:
                return

            if sym.isalpha():
                self.state_2()
            elif sym.isdigit():
                self.state_3()
            elif sym == '.':
                self.state_4()
            elif sym == '!':
                self.state_5()
            elif sym == '=':
                self.state_6()
            elif sym == '<':
                self.state_7()
            elif sym == '>':
                self.state_8()
            elif sym in [',', '\n', '+', '-', '*', '/', '(', ')', '[', ']', '{', '}', '?', ':']:
                self.state_9()
            else:
                self.error()

        pass

    def state_2(self):
        print("state2")
        sym = self.nextChar()
        print('[', sym, ']')

        if sym.isalpha() or sym.isdigit():
            self.state_2()

    def state_3(self):
        print("state3")
        sym = self.nextChar()
        print('[', sym, ']')

        if sym.isdigit():
            self.state_3()
        elif sym == '.':
            self.state_4()

    def state_4(self):
        print("stage4")
        sym = self.nextChar()
        print('[', sym, ']')

        if sym.isdigit():
            self.state_3()
        else:
            self.error()

    def state_5(self):
        print("stage5")
        sym = self.nextChar()
        print('[', sym, ']')

    def state_6(self):
        print("stage6")
        sym = self.nextChar()
        print('[', sym, ']')

    def state_7(self):
        print("stage7")
        sym = self.nextChar()
        print('[', sym, ']')

    def state_8(self):
        print("stage8")
        sym = self.nextChar()
        print('[', sym, ']')

    def state_9(self):
        print("state9")
