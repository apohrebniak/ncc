#! /usr/bin/python3.5

import sys

import ncc.draw as drw
import ncc.lexer as lxr
import ncc.parser as prsr


def main():
    stream = open(sys.argv[1])
    lexer = lxr.Lexer(stream)
    lexer.scan()

    drw.draw_lexeme_table(lexer.tokens)
    drw.draw_constants_table(list(lexer.constants.rows.values()))
    drw.draw_ids_table(list(lexer.ids.rows.values()))

    parser = prsr.Parser(lexer.tokens, lexer.ids, lexer.constants)
    parser.parse()



if __name__ == "__main__":
    main()
