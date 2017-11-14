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

        _, msg = self.program(0)

        print(msg)

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
        messages = []
        for prod in prods:
            is_production_valid = True
            for symbol in prod:
                if symbol in cmn.NOT_TERMINALS:

                    current_token_index, msg = self.functions[symbol](current_token_index)
                    if msg is not None:
                        messages.append(msg)
                        current_token_index = i
                        is_production_valid = False
                        break  # is production is invalid

                elif current_token_index < self.tokensLen and (
                    self.is_symbol(symbol, self.tokens[current_token_index].tag) or self.is_word(symbol,
                                self.tokens[current_token_index].tag)):
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
            if len(messages) == 1:
                return current_token_index, messages[0]
            else:
                return current_token_index, ""

        return current_token_index, None

    def program(self, i):
        prods = [["block"]]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a program at " + str(self.tokens[i].row_num)
        return res, msg

    def block(self, i):
        prods = [["{", "stmts", "}"],
                 ["{", "}"]]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a block" + str(self.tokens[i].row_num)
        return res, msg

    def statements(self, i):
        prods = [["stmt", "_stmts"]]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a stmts" + str(self.tokens[i].row_num)
        return res, msg

    def statements_trait(self, i):
        prods = [["\n", "stmts"],
                 []]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a stmts" + str(self.tokens[i].row_num)
        return res, msg

    def statement(self, i):
        prods = [["block"],
                 ["if", "log.expr", "?", "block", ":", "block"],
                 ["while", "log.expr", "do", "block"],
                 ["decl"],
                 ["id", "=", "expr"],
                 ["in", "(", "args", ")"],
                 ["out", "(", "args", ")"]]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a stmt" + str(self.tokens[i].row_num)
        return res, msg

    def declaration(self, i):
        prods = [["type", "_decl"]]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a decl" + str(self.tokens[i].row_num)
        return res, msg

    def declaration_trait(self, i):
        prods = [["id"],
                 ["id", "=", "expr"]]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a decl" + str(self.tokens[i].row_num)
        return res, msg

    def expression(self, i):
        prods = [["-", "term", "_expr"],
                 ["term", "_expr"]]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not an expr" + str(self.tokens[i].row_num)
        return res, msg

    def expression_trait(self, i):
        prods = [["+", "term", "_expr"],
                 ["-", "term", "_expr"],
                 []]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not an expr" + str(self.tokens[i].row_num)
        return res, msg

    def term(self, i):
        prods = [["factor", "_term"]]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a " + str(self.tokens[i].row_num)
        return res, msg

    def term_trait(self, i):
        prods = [["*", "factor", "_term"],
                 ["/", "factor", "_term"],
                 []]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a " + str(self.tokens[i].row_num)
        return res, msg

    def factor(self, i):
        prods = [["(", "expr", ")"],
                 ["id"],
                 ["const"]]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a " + str(self.tokens[i].row_num)
        return res, msg

    def log_expression(self, i):
        prods = [["log.expr", "_log.expr"]]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a " + str(self.tokens[i].row_num)
        return res, msg

    def log_expression_trait(self, i):
        prods = [["or", "log.term", "_log.expr"],
                 []]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a " + str(self.tokens[i].row_num)
        return res, msg

    def log_term(self, i):
        prods = [["log.factor", "_log.term"]]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a " + str(self.tokens[i].row_num)
        return res, msg

    def log_term_trait(self, i):
        prods = [["and", "log.factor", "_log.term"],
                 []]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a " + str(self.tokens[i].row_num)
        return res, msg

    def log_factor(self, i):  # TODO: this
        prods = [["not", "[","]"]]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a " + str(self.tokens[i].row_num)
        return res, msg

    def args(self, i):
        prods = [["id", "_args"]]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a " + str(self.tokens[i].row_num)
        return res, msg

    def args_trait(self, i):
        prods = [[",", "id", "_args"],
                 []]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a " + str(self.tokens[i].row_num)
        return res, msg

    def type(self, i):
        prods = [["int"],
                 ["float"]]

        res, msg = self.func(prods, i)
        if msg == "":
            msg = "Not a " + str(self.tokens[i].row_num)
        return res, msg

    def id(self, i):  # TODO
        prods = [["int"],
                 ["float"]]

        return i + 1, None

    def const(self, i):  # TODO
        prods = [["int"],
                 ["float"]]

        return i + 1, None
