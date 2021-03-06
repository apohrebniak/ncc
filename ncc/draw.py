import humanfriendly.tables as tbls

import ncc.common as cmn


def get_string_repr(d, tag):
    string = list(d.keys())[list(d.values()).index(tag)]
    if string == "\n":
        string = "\\n"
    return string


def draw_lexeme_table(tokens):
    print("L E X E M S")
    data = []
    for t in tokens:
        row = [t.row_num, t.tag]
        if hasattr(t, "payload"):
            str_value = "\\n" if t.payload == "\n" else t.payload
            row.append(str_value)
        elif t.tag in cmn.SYMBOLS.values():
            row.append(get_string_repr(cmn.SYMBOLS, t.tag))
        elif t.tag in cmn.WORDS.values():
            row.append(get_string_repr(cmn.WORDS, t.tag))
        row.append(t.index) if hasattr(t, "index") else row.append("")
        data.append(row)
    print(tbls.format_pretty_table(data, column_names=["Row", "Tag", "Payload",
                                                       "Index"]))


def draw_constants_table(constants):
    print("C O N S T A N T S")
    data = [[c.value, c.index] for c in constants]
    print(tbls.format_pretty_table(data, column_names=["Const", "Index"]))


def draw_ids_table(ids):
    print("ID")
    data = [[c.value, c.typeName, c.index] for c in ids]
    print(
        tbls.format_pretty_table(data, column_names=["Const", "Type", "Index"]))


def draw_rpn_build_table(rpn_stages):
    print("R P N  S T A G E S")
    data = [["\\n" if s.lexeme == "\n" else s.lexeme, s.stack, s.rpn] for s in rpn_stages]
    print(tbls.format_pretty_table(data, column_names=["Lexeme", "Stack", "RPN"]))
