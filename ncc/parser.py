import ncc.common as cmn
import ncc.my_token as tkn


class Syntaxer:
    def __init__(self, ids, consts):
        self.tokens = None
        self.ids = ids
        self.consts = consts
        self.tokensLen = 0
        self.functions = {"program": self.program,
                          "block": self.block,
                          "stmts": self.statements,
                          "_stmts": self.statements_trait,
                          "stmt": self.statement,
                          "decl": self.declaration,
                          "_decl": self.declaration_trait,
                          "__decl": self.declaration_trait_trait,
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
                          "_log.factor": self.log_factor_trait,
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

        _, error_token = self.program(0)

        if error_token is not None:
            print("Error at row: {}".format(self.tokens[error_token].row_num))
        else:
            print("Correct syntax")

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
        max_token_where_error_occurred = None
        is_any_symbol_from_any_production_succeded = False
        for prod in prods:
            is_production_valid = True
            for symbol in prod:

                # Seems like, if error occurred if token witch index is lower or equals to current index + 1
                # then empty production is acceptable. lulz let it be for now
                if symbol is None and not is_any_symbol_from_any_production_succeded:
                    break
                    # if max_token_where_error_occurred is not None:
                    #     if current_token_index + 1 >= max_token_where_error_occurred:
                    #         break
                    # else:
                    #     break

                if symbol in cmn.NOT_TERMINALS:

                    current_token_index, error_token_index = self.functions[symbol](current_token_index)
                    if error_token_index is not None:
                        max_token_where_error_occurred = max([max_token_where_error_occurred, error_token_index]) \
                            if max_token_where_error_occurred is not None else error_token_index
                        current_token_index = i
                        is_production_valid = False
                        break  # is production is invalid

                elif current_token_index < self.tokensLen and (
                            self.is_symbol(symbol, self.tokens[current_token_index].tag) or self.is_word(symbol,
                                                                                                         self.tokens[
                                                                                                             current_token_index].tag)):
                    current_token_index += 1
                else:
                    current_token_index = i
                    is_production_valid = False
                    break  # is production is invalid

                is_any_symbol_from_any_production_succeded = True

            if is_production_valid:
                is_production_found = True
                break

        # check if production is found
        if not is_production_found:
            # production wasn't found. return an error token index
            if max_token_where_error_occurred is not None and current_token_index < max_token_where_error_occurred:
                return current_token_index, max_token_where_error_occurred
            else:
                return current_token_index, current_token_index
        else:
            # seems good
            return current_token_index, None

    def program(self, i):
        prods = [["block"]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def block(self, i):
        prods = [["{", "stmts", "}"],
                 ["{", "}"]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def statements(self, i):
        prods = [["\n", "stmt", "_stmts"]]

        res, error_token = self.func(prods, i)

        return res, error_token

    def statements_trait(self, i):
        prods = [["stmts", "_stmts"],
                 [None]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def statement(self, i):
        prods = [["block"],
                 ["if", "log.expr", "?", "block", ":", "block"],
                 ["while", "log.expr", "do", "block"],
                 ["decl"],
                 ["id", "=", "expr"],
                 ["in", "(", "args", ")"],
                 ["out", "(", "args", ")"]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def declaration(self, i):
        prods = [["type", "_decl"]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def declaration_trait(self, i):
        prods = [["id", "__decl"]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def declaration_trait_trait(self, i):
        prods = [["=", "expr"],
                 [None]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def expression(self, i):
        prods = [["-", "term", "_expr"],
                 ["term", "_expr"]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def expression_trait(self, i):
        prods = [["+", "term", "_expr"],
                 ["-", "term", "_expr"],
                 [None]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def term(self, i):
        prods = [["factor", "_term"]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def term_trait(self, i):
        prods = [["*", "factor", "_term"],
                 ["/", "factor", "_term"],
                 [None]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def factor(self, i):
        prods = [["(", "expr", ")"],
                 ["id"],
                 ["const"]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def log_expression(self, i):
        prods = [["log.term", "_log.expr"]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def log_expression_trait(self, i):
        prods = [["or", "log.term", "_log.expr"],
                 [None]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def log_term(self, i):
        prods = [["log.factor", "_log.term"]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def log_term_trait(self, i):
        prods = [["and", "log.factor", "_log.term"],
                 [None]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def log_factor(self, i):  # TODO: this
        prods = [["not", "[", "log.expr", "]"],
                 ["not", "expr", "_log.factor"],
                 ["[", "log.expr", "]"],
                 ["expr", "_log.factor"]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def log_factor_trait(self, i):
        prods = [[">", "expr"],
                 [">=", "expr"],
                 ["<", "expr"],
                 ["<=", "expr"],
                 ["==", "expr"],
                 ["!=", "expr"]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def args(self, i):
        prods = [["id", "_args"]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def args_trait(self, i):
        prods = [[",", "id", "_args"],
                 [None]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def type(self, i):
        prods = [["int"],
                 ["float"]]

        res, error_token = self.func(prods, i)
        return res, error_token

    def id(self, i):
        token = self.tokens[i]
        if isinstance(token, tkn.Word) and self.ids.contains_value(token.payload):
            return i + 1, None
        else:
            return i, i

    def const(self, i):
        token = self.tokens[i]
        if isinstance(token, tkn.Constant) and self.consts.contains_value(token.payload):
            return i + 1, None
        else:
            return i, i
