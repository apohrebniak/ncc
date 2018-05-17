import sys

import ncc.common as cmn
import ncc.lexer_token as tkn

"""Recursive descend parser"""


class Parser():
    def __init__(self, tokens, idsTable, constTable):
        self.tokens = tokens
        self.ids = idsTable
        self.consts = constTable
        self.symbols = {v: k for k, v in cmn.SYMBOLS.items()}
        self.words = {v: k for k, v in cmn.WORDS.items()}

    def parse(self):
        self.is_program(0)

    def is_program(self, i):
        curr_index = i
        return self.is_block(curr_index)

    def is_block(self, i):
        curr_index = i
        if self.get_token_tag(curr_index) == cmn.SYMBOLS["{"]:

            # empty block
            if self.get_token_tag(curr_index + 1) == cmn.SYMBOLS["}"]:
                return curr_index + 2, True
            else:
                index, res = self.is_stmts(curr_index + 1)
                if not res:
                    self.error("Not a statement", curr_index + 1)
                else:
                    curr_index = index

            # stmts
            if self.get_token_tag(curr_index) == cmn.SYMBOLS["}"]:
                return curr_index + 1, True
            else:
                self.error("'}' expected", curr_index)

        else:
            return curr_index, False

    def is_stmts(self, i):
        curr_index = i

        # statement
        index, res = self.is_stmt(curr_index)
        if res:
            curr_index = index

        # statements
        while self.get_token_tag(curr_index) == cmn.SYMBOLS["\n"]:
            index, res = self.is_stmts(curr_index + 1)
            if res:
                curr_index = index
            else:
                return curr_index + 1, False

        return curr_index, True

    def is_stmt(self, i):
        curr_index = i
        # block
        index, res = self.is_block(curr_index)
        if not res:
            # if
            index, res = self.is_stmt_if(curr_index)
            if not res:
                # while
                index, res = self.is_stmt_while(curr_index)
                if not res:
                    # decl
                    index, res = self.is_stmt_decl(curr_index)
                    if not res:
                        # assing
                        index, res = self.is_stmt_assign(curr_index)
                        if not res:
                            # in
                            index, res = self.is_stmt_in(curr_index)
                            if not res:
                                # out
                                index, res = self.is_stmt_out(curr_index)
                                if not res:
                                    # error
                                    self.cannot_resolve_symbol_at(curr_index)
        return index, True

    def is_stmt_if(self, i):
        curr_index = i
        if self.get_token_tag(curr_index) == cmn.WORDS["if"]:
            index, res = self.is_log_expr(curr_index + 1)
            if res:
                curr_index = index
                if self.get_token_tag(curr_index) == cmn.SYMBOLS["?"]:
                    index, res = self.is_block(curr_index + 1)
                    if res:
                        curr_index = index
                        if self.get_token_tag(curr_index) == cmn.SYMBOLS[":"]:
                            index, res = self.is_block(curr_index + 1)
                            if res:
                                curr_index = index
                                return curr_index, True
                            else:
                                self.error("'{' expected", curr_index + 1)
                        else:
                            self.error("':' expected", curr_index)
                    else:
                        self.error("'{' expected", curr_index + 1)
                else:
                    self.error("'?' expected", curr_index)
            else:
                self.error("'[' expression expected", curr_index + 1)
        return i, False

    def is_stmt_while(self, i):
        curr_index = i
        if self.get_token_tag(curr_index) == cmn.WORDS["while"]:
            index, res = self.is_log_expr(curr_index + 1)
            if res:
                curr_index = index
                if self.get_token_tag(curr_index) == cmn.WORDS["do"]:
                    index, res = self.is_block(curr_index + 1)
                    if res:
                        curr_index = index
                        return curr_index, True
                    else:
                        self.error("Block expected", curr_index + 1)
                else:
                    self.error("'do' expected", curr_index)
            else:
                self.error("Logic expression expected", curr_index + 1)
        return i, False

    def is_stmt_decl(self, i):
        curr_index = i
        index, res = self.is_type(curr_index)
        if res:
            curr_index = index
            index, res = self.is_id(curr_index)
            if res:
                curr_index = index
                if self.get_token_tag(curr_index) == cmn.SYMBOLS["="]:
                    index, res = self.is_expr(curr_index + 1)
                    if res:
                        curr_index = index
                        return curr_index, True
                    else:
                        self.error("Expression expected", curr_index + 1)
                else:
                    return curr_index, True
            else:
                self.error("Variable expected", curr_index)
        return i, False

    def is_stmt_assign(self, i):
        curr_index = i
        index, res = self.is_id(curr_index)
        if res:
            curr_index = index
            if self.get_token_tag(curr_index) == cmn.SYMBOLS["="]:
                index, res = self.is_expr(curr_index + 1)
                if res:
                    curr_index = index
                    return curr_index, True
                else:
                    self.error("Expression expected", curr_index + 1)
            else:
                self.error("'=' expected", curr_index)
        return i, False

    def is_stmt_in(self, i):
        curr_index = i
        if self.get_token_tag(curr_index) == cmn.WORDS["in"]:
            if self.get_token_tag(curr_index + 1) == cmn.SYMBOLS["("]:
                index, res = self.is_args(curr_index + 2)
                if res:
                    curr_index = index
                    if self.get_token_tag(curr_index) == cmn.SYMBOLS[")"]:
                        return curr_index + 1, True
                    else:
                        self.error("')' expected", curr_index)
                else:
                    self.error("Arguments expected", curr_index + 1)
            else:
                self.error("'(' expected", curr_index + 1)

        return i, False

    def is_stmt_out(self, i):
        curr_index = i
        if self.get_token_tag(curr_index) == cmn.WORDS["out"]:
            if self.get_token_tag(curr_index + 1) == cmn.SYMBOLS["("]:
                index, res = self.is_args(curr_index + 2)
                if res:
                    curr_index = index
                    if self.get_token_tag(curr_index) == cmn.SYMBOLS[")"]:
                        return curr_index + 1, True
                    else:
                        self.error("')' expected", curr_index)
                else:
                    self.error("Arguments expected", curr_index + 2)
            else:
                self.error("'(' expected", curr_index + 1)

        return i, False

    def is_expr(self, i):
        curr_index = i
        if self.get_token_tag(curr_index) == cmn.SYMBOLS["-"]:
            curr_index += 1
        index, res = self.is_term(curr_index)
        if res:
            curr_index = index
            while self.get_token_tag(curr_index) == cmn.SYMBOLS["+"] or \
                    self.get_token_tag(curr_index) == cmn.SYMBOLS["-"]:
                index, res = self.is_term(curr_index + 1)
                if res:
                    curr_index = index
                    return curr_index, True
                else:
                    self.error("Expression expected", curr_index + 1)

            return curr_index, True

        return i, False

    def is_term(self, i):
        curr_index = i
        index, res = self.is_factor(curr_index)
        if res:
            curr_index = index
            while self.get_token_tag(curr_index) == cmn.SYMBOLS["*"] or \
                    self.get_token_tag(curr_index) == cmn.SYMBOLS["/"]:
                index, res = self.is_factor(curr_index + 1)
                if res:
                    curr_index = index
                    return curr_index, True
                else:
                    self.error("Expression expected", curr_index + 1)

            return curr_index, True

        return i, False

    def is_factor(self, i):
        curr_index = i
        index, res = self.is_id(curr_index)
        if not res:
            index, res = self.is_const(curr_index)
            if not res:
                if self.get_token_tag(curr_index) == cmn.SYMBOLS["("]:
                    index, res = self.is_expr(curr_index + 1)
                    if res:
                        curr_index = index
                        if self.get_token_tag(curr_index) == cmn.SYMBOLS[")"]:
                            return curr_index + 1, True
                        else:
                            self.error("')' expected", curr_index)
                    else:
                        self.error("Expression expected", curr_index + 1)
                else:
                    return curr_index, False
        return index, True

    def is_log_expr(self, i):
        curr_index = i
        index, res = self.is_log_term(curr_index)
        if res:
            curr_index = index
            while self.get_token_tag(curr_index) == cmn.WORDS["or"]:
                index, res = self.is_log_term(curr_index + 1)
                if res:
                    curr_index = index
                else:
                    self.error("Logic expression expected", curr_index + 1)
            return curr_index, True
        return i, False

    def is_log_term(self, i):
        curr_index = i
        index, res = self.is_log_factor(curr_index)
        if res:
            curr_index = index
            while self.get_token_tag(curr_index) == cmn.WORDS["and"]:
                index, res = self.is_log_factor(curr_index + 1)
                if res:
                    curr_index = index
                else:
                    self.error("Logic expression expected", curr_index + 1)
            return curr_index, True
        return i, False

    def is_log_factor(self, i):
        curr_index = i
        while self.get_token_tag(curr_index) == cmn.WORDS["not"]:
            curr_index += 1

        if self.get_token_tag(curr_index) == cmn.SYMBOLS["["]:
            index, res = self.is_log_expr(curr_index + 1)
            if res:
                curr_index = index
                if self.get_token_tag(curr_index) == cmn.SYMBOLS["]"]:
                    return curr_index + 1, True
                else:
                    self.error("']' expected", curr_index)
            else:
                self.error("Logic expression expected", curr_index + 1)
        else:
            index, res = self.is_expr(curr_index)
            if res:
                curr_index = index
                while self.get_token_tag(curr_index) in [cmn.SYMBOLS[">"],
                                                         cmn.SYMBOLS["<"],
                                                         cmn.SYMBOLS[">="],
                                                         cmn.SYMBOLS["<="],
                                                         cmn.SYMBOLS["=="],
                                                         cmn.SYMBOLS["!="]]:
                    index, res = self.is_expr(curr_index + 1)
                    if res:
                        curr_index = index
                    else:
                        self.error("Expression expected", curr_index + 1)
                return curr_index, True
            else:
                return curr_index, False

    def is_args(self, i):
        curr_index = i
        index, res = self.is_id(curr_index)
        if res:
            curr_index = index
            while self.get_token_tag(curr_index) == cmn.SYMBOLS[","]:
                index, res = self.is_id(curr_index + 1)
                if res:
                    curr_index = index
                else:
                    return curr_index + 1, False
            return curr_index, True
        return i, False

    def is_type(self, i):
        curr_index = i
        if self.get_token_tag(curr_index) == cmn.WORDS["int"] or \
                self.get_token_tag(curr_index) == cmn.WORDS["float"]:
            return curr_index + 1, True
        return i, False

    def is_id(self, i):
        token = self.tokens[i]
        if isinstance(token, tkn.Identity) and self.ids.contains_value(
            token.payload):
            return i + 1, True
        else:
            return i, False

    def is_const(self, i):
        token = self.tokens[i]
        if isinstance(token, tkn.Constant) and self.consts.contains_value(
            token.payload):
            return i + 1, True
        else:
            return i, False

    def get_token_tag(self, index):
        if index >= len(self.tokens):
            return cmn.SYMBOLS["@"]
        return self.tokens[index].tag

    def error(self, message, index):
        token = self.tokens[index] if index < len(self.tokens) else self.tokens[
            -1]
        print(message, "at {}:{}".format(token.row_num, token.column_num))
        sys.exit(1)

    def cannot_resolve_symbol_at(self, index):
        token = self.tokens[index]
        self.error("Cannot resolve symbol '{}'".format(token.payload), index)
