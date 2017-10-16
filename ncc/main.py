#python3.5

import sys
import ncc.Lexer as Lexer


def main():
    stream = open(sys.argv[1])
    lexer = Lexer.Lexer(stream)
    lexer.scan()


if __name__ == "__main__":
    main()