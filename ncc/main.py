#! /usr/bin/python3.5

import sys

import ncc.draw as drw
import ncc.lexer as lxr
import ncc.parser_auto as prsr_auto


def main():
    stream = open(sys.argv[1])  # input stream

    # scan input stream
    lexer = lxr.Lexer(stream)
    lexer.scan()

    # draw tables
    drw.draw_lexeme_table(lexer.tokens)
    drw.draw_constants_table(list(lexer.constants.rows.values()))
    drw.draw_ids_table(list(lexer.ids.rows.values()))

    # parser = prsr.Parser(lexer.tokens, lexer.ids, lexer.constants)
    # parser.parse()

    parserAuto = prsr_auto.ParserAuto(lexer.tokens, lexer.ids, lexer.constants)
    parserAuto.parse()


if __name__ == "__main__":
    main()
