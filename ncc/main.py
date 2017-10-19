#python3.5

import sys
import ncc.Lexer as Lexer
import ncc.Token

def main():
    stream = open(sys.argv[1])
    lexer = Lexer.Lexer(stream)
    lexer.scan()
    print("=================")
    print("TABLE")
    print("=================")
    for token in lexer.tokens:
        if isinstance(token, ncc.Token.Word):
            print(token.tag, token.row_num, token.lexeme, token.index)
        elif isinstance(token, ncc.Token.Constant):
            print(token.tag, token.row_num, token.value, token.index)
        else:
            print(token.tag, token.row_num)
    print("=================")
    print("CONSTANTS")
    print("=================")
    print(lexer.constants)
    print("=================")
    print("IDS")
    print("=================")
    print(lexer.ids)

if __name__ == "__main__":
    main()