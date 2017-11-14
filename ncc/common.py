LSB, RSB, LFB, RFB, LB, RB, WHILE, DO, IN, OUT, OR, AND, NOT, \
INT, FLOAT, IF, DOTS, EQ, PLUS, MINUS, MUL, DIV, NEQ, LOW, LOWEQ, \
HI, HIEQ, ID, CONST, NL, QM, COMMA = range(32)

SYMBOLS = {'[': LSB, ']': RSB, '{': LFB, '}': RFB, '(': LB, ')': RB,
           ':': DOTS, '=': EQ, '+': PLUS, '-': MINUS, '*': MUL, '/': DIV,
           '!=': NEQ, '<': LOW, '<=': LOWEQ, '>': HI, '>=': HIEQ, '\n': NL, '?': QM, ",": COMMA}

WORDS = {"if": IF, "while": WHILE, "do": DO, "in": IN, "out": OUT, "or": OR,
         "and": AND, "not": NOT, "int": INT, "float": FLOAT}

TYPES = {INT: "int", FLOAT: "float"}

PROGRAM, BLOCK, STMTS, _STMTS, STMT, DECL, _DECL, EXPR, _EXPR, TERM, _TERM, FACTOR, \
LOG_EXPR, _LOG_EXPR, LOG_TERM, _LOG_TERM, LOG_FACTOR, ARGS, _ARGS, TYPE, _ID, CONSTANT = range(22)

NOT_TERMINALS = {"program": PROGRAM, "block": BLOCK, "stmts": STMTS, "_stmts": _STMTS,
                 "stmt": STMT, "decl": DECL, "_decl": DECL, "expr": EXPR, "_expr": _EXPR,
                 "term": TERM, "_term": _TERM, "factor": FACTOR, "log.expr": LOG_EXPR,
                 "_log.expr": _LOG_EXPR, "log.term": LOG_TERM, "_log.term": _LOG_TERM,
                 "log.factor": LOG_FACTOR, "args": ARGS, "_args": _ARGS, "type": TYPE, "id": _ID, "const": CONSTANT}


def get_key_by_value(d, tag):
    string = list(d.keys())[list(d.values()).index(tag)]
    if string == "\n":
        string = "\\n"
    return string
