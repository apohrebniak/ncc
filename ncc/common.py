# lexer and parser specific symbols
LSB, RSB, LFB, RFB, LB, RB, WHILE, DO, IN, OUT, OR, AND, NOT, \
INT, FLOAT, IF, DOTS, ASSIGN, PLUS, MINUS, MUL, DIV, EQ, NEQ, LOW, LOWEQ, \
HI, HIEQ, ID, CONST, NL, QM, COMMA, WRONG = range(34)

SYMBOLS = {
    '[': LSB, ']': RSB, '{': LFB, '}': RFB, '(': LB, ')': RB,
    ':': DOTS, '=': ASSIGN, '+': PLUS, '-': MINUS, '*': MUL, '/': DIV,
    "==": EQ,
    '!=': NEQ, '<': LOW, '<=': LOWEQ, '>': HI, '>=': HIEQ, '\n': NL,
    '?': QM, ",": COMMA, "@": WRONG
}

WORDS = {
    "if": IF, "while": WHILE, "do": DO, "in": IN, "out": OUT, "or": OR,
    "and": AND, "not": NOT, "int": INT, "float": FLOAT
}

TYPES = {
    INT: "int", FLOAT: "float"
}

# RPN specific symbols
R_ALB, R_ARB, R_PLUS, R_MINUS, R_MUL, R_DIV, R_LFB, R_RFB, \
    R_INT, R_FLOAT, R_ASSGN = range(11)

RPN_SYMBOLS = {
    '(': R_ALB, ')': R_ARB, '{': R_LFB, '}': R_RFB
}

RPN_OPERATORS = {
    '+': R_PLUS, '-': R_MINUS, '*': R_MUL,
    '/': R_DIV, 'int': R_INT, 'float': R_FLOAT, '=': R_ASSGN
}

RPN_PRIORITIES = {R_LFB: 0, R_RFB: 1, R_ASSGN: 3, R_ALB: 3, R_INT: 3, R_FLOAT: 3, R_ARB: 4, R_PLUS: 8, R_MINUS: 8, R_MUL: 9, R_DIV: 9}
