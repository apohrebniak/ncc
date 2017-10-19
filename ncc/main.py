#python3.5

import sys
import ncc.Lexer as Lexer
import ncc.Token

def main():
    stream = open(sys.argv[1])
    lexer = Lexer.Lexer(stream)
    lexer.scan()
    # print(lexer.constants)
    print(lexer.ids)

if __name__ == "__main__":
    main()