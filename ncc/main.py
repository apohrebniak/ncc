#! /usr/bin/python3.5

import argparse
import sys

import ncc.dijkstra as djk
import ncc.draw as drw
import ncc.interpreter as inter
import ncc.lexer as lxr
import ncc.parser as prsr


# import ncc.draw as drw


def main():
    argparser = argparse.ArgumentParser(description="NCC compiler")
    argparser.add_argument("FILE", help="file to be executed")
    argparser.add_argument("--lex", action='store_true',
                           help='show lexems table')
    argparser.add_argument("--var", action='store_true', help='show vars table')
    argparser.add_argument("--const", action='store_true',
                           help='show const table')
    argparser.add_argument("--rpn", action='store_true',
                           help='show full RPN string')
    argparser.add_argument("--rpnt", action='store_true',
                           help='show RPN building table')
    argparser.add_argument("--parse", action='store_true', default=False,
                           help='parse only mode')
    args = argparser.parse_args()

    stream = open(args.FILE)  # input stream

    # STAGE 1
    # scan input stream
    lexer = lxr.Lexer(stream)
    lexer.scan()

    tokens = lexer.tokens

    # draw tables
    if args.lex:
        drw.draw_lexeme_table(lexer.tokens)
    if args.const:
        drw.draw_constants_table(list(lexer.constants.rows.values()))
    if args.var:
        drw.draw_ids_table(list(lexer.ids.rows.values()))

    # STAGE 2
    # parser
    parser = prsr.Parser(lexer.tokens, lexer.ids, lexer.constants)
    parser.parse()

    # STAGE 3
    # dijkstra
    rpnBuilder = djk.DijkstraRPNBuilder(tokens)
    rpn = rpnBuilder.build_rpn()

    if args.parse:
        sys.exit(0)

    # STAGE 4
    # interpreter
    interpreter = inter.Interpreter(rpn)
    interpreter.run()


if __name__ == "__main__":
    main()
