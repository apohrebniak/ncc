#! /usr/bin/python3.5

import sys

import ncc.lexer as lxr
import ncc.parser as prsr
import ncc.dijkstra as djk
# import ncc.draw as drw


def main():
    stream = open(sys.argv[1])  # input stream

    # scan input stream
    lexer = lxr.Lexer(stream)
    lexer.scan()

    tokens = lexer.tokens

    # draw tables
    # drw.draw_lexeme_table(lexer.tokens)
    # drw.draw_constants_table(list(lexer.constants.rows.values()))
    # drw.draw_ids_table(list(lexer.ids.rows.values()))

    parser = prsr.Parser(lexer.tokens, lexer.ids, lexer.constants)
    parser.parse()

    # parserAuto = prsr_auto.ParserAuto(lexer.tokens, lexer.ids, lexer.constants)
    # parserAuto.parse()

    #dijkstra
    rpnBuilder = djk.DijkstraRPNBuilder(tokens)
    rpn = rpnBuilder.build_rpn()
    print(rpn)
    assert "[one, int, 1, =, N, int, N, count_1, in, N, 1, <=, lbl_0, JMPF, N, one, count_2, out, lbl_1, JMP, lbl_0, factorial, int, N, =, lbl_2, N, 1, >, lbl_3, JMPF, N, N, 1, -, =, factorial, factorial, N, *, =, lbl_2, JMP, lbl_3, N, factorial, count_2, out, lbl_1]" == repr(rpn)


if __name__ == "__main__":
    main()
