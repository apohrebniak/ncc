#python3.5

import sys
import ncc.Lexer as Lexer
import ncc.Token

def main():
    stream = open(sys.argv[1])
    lexer = Lexer.Lexer(stream)
    lexer.scan()
    print("table")
    for token in lexer.tokens:
        if isinstance(token, ncc.Token.Word):
            print(token.tag, token.lexeme, token.index)
        elif isinstance(token, ncc.Token.Constant):
            print(token.tag, token.value, token.index)
        else:
            print(token.tag)
    print("table of constants")
    print(lexer.constants)
    print("table of ids")
    print(lexer.ids)

if __name__ == "__main__":
    main()