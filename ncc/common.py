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
R_EQ, R_NEQ, R_HIEQ, R_LOWEQ, R_LSB, R_RSB, R_IF, R_QM, R_DOTS,\
R_JMP, R_JMPF, R_WHILE, R_DO = range(29)

RPN_SYMBOLS = {
    '(': R_ALB, ')': R_ARB,
    '{': R_LFB, '}': R_RFB,
    '[': R_LSB, ']': R_RSB
}

RPN_OPERATORS = {
    '+': R_PLUS, '-': R_MINUS, '*': R_MUL,
    '/': R_DIV, 'int': R_INT, 'float': R_FLOAT, '=': R_ASSGN,
    'or': R_OR, 'and': R_AND, 'not': R_NOT, '>': R_HI, '<': R_LOW,
    '==': R_EQ, '!=': R_NEQ, '>=': R_HIEQ, '<=': R_LOWEQ,
    'if': R_IF, '?': R_QM, ':': R_DOTS, 'while': R_WHILE, 'do': R_DO
}

RPN_PRIORITIES = {R_LFB: 0,
                  R_RFB: 1,
                  R_IF: 2, R_WHILE: 2,
                  R_QM: 3, R_DOTS: 3, R_DO: 3,
                  R_LSB: 4,
                  R_RSB: 5,
                  R_ASSGN: 6, R_ALB: 6, R_INT: 6, R_FLOAT: 6,
                  R_ARB: 7, R_OR: 7,
                  R_AND: 8,
                  R_NOT: 9,
                  R_LOW: 10, R_HI: 10, R_EQ: 10, R_NEQ: 10, R_LOWEQ: 10,R_HIEQ: 10,
                  R_PLUS: 11, R_MINUS: 11,
                  R_MUL: 12, R_DIV: 12
                  }
