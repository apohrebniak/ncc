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
R_INT, R_FLOAT, R_ASSGN, R_OR, R_AND, R_NOT, R_LOW, R_HI, \
R_EQ, R_NEQ, R_HIEQ, R_LOWEQ, R_LSB, R_RSB, R_IF, R_QM, R_DOTS, \
R_JMP, R_JMPF, R_WHILE, R_DO, R_NL, R_IN, R_OUT, R_COMMA = range(33)

RPN_SYMBOLS = {
    '(': R_ALB, ')': R_ARB,
    '{': R_LFB, '}': R_RFB,
    '[': R_LSB, ']': R_RSB,
    '\n': R_NL,
    ',': R_COMMA
}

RPN_OPERATORS = {
    '+': R_PLUS, '-': R_MINUS, '*': R_MUL,
    '/': R_DIV, 'int': R_INT, 'float': R_FLOAT, '=': R_ASSGN,
    'or': R_OR, 'and': R_AND, 'not': R_NOT, '>': R_HI, '<': R_LOW,
    '==': R_EQ, '!=': R_NEQ, '>=': R_HIEQ, '<=': R_LOWEQ,
    'if': R_IF, '?': R_QM, ':': R_DOTS, 'while': R_WHILE, 'do': R_DO,
    'in': R_IN, 'out': R_OUT
}

RPN_PRIORITIES = {R_LFB: 0,
                  R_RFB: 1,
                  R_NL: 2,
                  R_IF: 3, R_WHILE: 3, R_IN: 3, R_OUT: 3,
                  R_QM: 4, R_DOTS: 4, R_DO: 4,
                  R_LSB: 5,
                  R_RSB: 6,
                  R_ASSGN: 7, R_ALB: 7, R_INT: 7, R_FLOAT: 7,
                  R_ARB: 8, R_OR: 8,
                  R_AND: 9,
                  R_NOT: 10,
                  R_LOW: 11, R_HI: 11, R_EQ: 11, R_NEQ: 11, R_LOWEQ: 11,
                  R_HIEQ: 11,
                  R_PLUS: 12, R_MINUS: 12,
                  R_MUL: 13, R_DIV: 13
                  }
