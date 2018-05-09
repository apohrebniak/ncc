LSB, RSB, LFB, RFB, LB, RB, WHILE, DO, IN, OUT, OR, AND, NOT, \
INT, FLOAT, IF, DOTS, ASSIGN, PLUS, MINUS, MUL, DIV, EQ, NEQ, LOW, LOWEQ, \
HI, HIEQ, ID, CONST, NL, QM, COMMA, WRONG = range(34)

SYMBOLS = {'[': LSB, ']': RSB, '{': LFB, '}': RFB, '(': LB, ')': RB,
           ':': DOTS, '=': ASSIGN, '+': PLUS, '-': MINUS, '*': MUL, '/': DIV, "==": EQ,
           '!=': NEQ, '<': LOW, '<=': LOWEQ, '>': HI, '>=': HIEQ, '\n': NL,
           '?': QM, ",": COMMA, "@": WRONG}

WORDS = {"if": IF, "while": WHILE, "do": DO, "in": IN, "out": OUT, "or": OR,
         "and": AND, "not": NOT, "int": INT, "float": FLOAT}

TYPES = {INT: "int", FLOAT: "float"}
