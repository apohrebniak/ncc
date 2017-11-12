import sys

import ncc.common as cmn


class Syntaxer:
    def __init__(self):
        self.tokens = None
        self.tokensLen = 0
        self.functions = {"program": self.program,
                          "block": self.block,
                          "stmts": self.statements,
                          "_stmts": self.statements_trait,
                          "stmt": self.statement,
                          "decl": self.declaration,
                          "_decl": self.declaration_trait,
                          "expr": self.expression,
                          "_expr": self.expression_trait,
                          "term": self.term,
                          "_term": self.term_trait,
                          "factor": self.factor,
                          "log.expr": self.log_expression,
                          "_log.expr": self.log_expression_trait,
                          "log.term": self.log_term,
                          "_log.term": self.log_term_trait,
                          "log.factor": self.log_factor,
                          "args": self.args,
                          "_args": self.args_trait,
                          "type": self.type,
                          "id": self.id,
                          "const": self.const}
        self.symbols_by_tag = {v: k for k, v in cmn.SYMBOLS.items()}
        self.words_by_tag = {v: k for k, v in cmn.WORDS.items()}

    def analyze_tokens(self, tokens):
        self.tokens = tokens
        self.tokensLen = len(tokens)

        self.program(0)

    def is_symbol(self, symbol, tag):
        if tag in self.symbols_by_tag:
            return symbol == self.symbols_by_tag[tag]
        else:
            False

    def is_word(self, symbol, tag):
        if tag in self.words_by_tag:
            return symbol == self.words_by_tag[tag]
        else:
            False

    def func(self, prods, i):
        current_token_index = i
        is_production_found = False
        for prod in prods:
            is_production_valid = True
            for symbol in prod:
                if symbol in cmn.NOT_TERMINALS:
                    current_token_index = self.functions[symbol](current_token_index)
                elif current_token_index < self.tokensLen and (self.is_symbol(symbol, self.tokens[current_token_index].tag)
                                                               or self.is_word(symbol, self.tokens[current_token_index].tag)):  # TODO: if symbol is current token symbol
                    current_token_index += 1
                else:
                    current_token_index = i
                    is_production_valid = False
                    break  # is production is invalid
            if is_production_valid:
                is_production_found = True
                break
        # check if production is found
        if not is_production_found:
            raise Exception()
        return current_token_index

    def program(self, i):
        prods = [["block"]]

        return self.func(prods, i)

    def block(self, i):
        prods = [["{", "stmts", "}"],
                 ["{", "}"]]

        return self.func(prods, i)

    def statements(self, i):
        prods = [["stmt"],
                 ["_stmts"]]

        return self.func(prods, i)

    def statements_trait(self, i):
        prods = [["\n", "stmt"],
                 []]

        return self.func(prods, i)

    def statement(self, i):
        prods = [["block"],
                 ["if", "log.expr", "?", "block", ":", "block"],
                 ["while", "log.expr", "do", "block"],
                 ["decl"],
                 ["id", "=", "expr"],
                 ["in", "(", "args", ")"],
                 ["out", "(", "args", ")"]]

        return self.func(prods, i)

    def declaration(self, i):
        prods = [["type"],
                 ["_decl"]]

        return self.func(prods, i)

    def declaration_trait(self, i):
        prods = [["id"],
                 ["id", "=", "expr"]]

        return self.func(prods, i)

    def expression(self, i):
        prods = [["-", "term", "_expr"],
                 ["term", "_expr"]]

        return self.func(prods, i)

    def expression_trait(self, i):
        prods = [["+", "term", "_expr"],
                 ["-", "term", "_expr"],
                 []]

        return self.func(prods, i)

    def term(self, i):
        prods = [["factor", "_term"]]

        return self.func(prods, i)

    def term_trait(self, i):
        prods = [["*", "factor", "_term"],
                 ["/", "factor", "_term"]]

        return self.func(prods, i)

    def factor(self, i):
        prods = [["(", "expr", ")"],
                 ["id"],
                 ["const"]]

        return self.func(prods, i)

    def log_expression(self, i):
        prods = [["log.expr", "_log.expr"]]

        return self.func(prods, i)

    def log_expression_trait(self, i):
        prods = [["or", "log.term", "_log.expr"],
                 []]

        return self.func(prods, i)

    def log_term(self, i):
        prods = [["log.factor", "_log.term"]]

        return self.func(prods, i)

    def log_term_trait(self, i):
        prods = [["and", "log.factor", "_log.term"],
                 []]

        return self.func(prods, i)

    def log_factor(self, i): # TODO: this
        prods = [["stmts"], ["_stmts"]]

        return self.func(prods, i)

    def args(self, i):
        prods = [["id", "_args"]]

        return self.func(prods, i)

    def args_trait(self, i):
        prods = [[",", "id", "_args"],
                 []]

        return self.func(prods, i)

    def type(self, i):
        prods = [["int"],
                 ["float"]]

        return self.func(prods, i)

    def id(self, i): # TODO
        prods = [["int"],
                 ["float"]]

        return i + 1

    def const(self, i): # TODO
        prods = [["int"],
                 ["float"]]

        return i + 1
