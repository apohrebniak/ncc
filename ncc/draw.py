import humanfriendly.tables as tbls

import ncc.common as cmn


def get_string_repr(d, tag):
    string = list(d.keys())[list(d.values()).index(tag)]
    if string == "\n":
        string = ""
    return string


def draw_lexeme_table(tokens):
    print("L E X E M S")
    data = []
    for t in tokens:
        row = [t.row_num, t.tag]
        if hasattr(t, "payload"):
            row.append(t.payload)
        elif t.tag in cmn.SYMBOLS.values():
            row.append(get_string_repr(cmn.SYMBOLS, t.tag))
        elif t.tag in cmn.WORDS.values():
            row.append(get_string_repr(cmn.WORDS, t.tag))
        row.append(t.index) if hasattr(t, "index") else row.append("")
        data.append(row)
    print(tbls.format_pretty_table(data, column_names=["Row", "Tag", "Payload", "Index"]))


def draw_constants_table(constants):
    print("C O N S T A N T S")
    data = [[c.value, c.index] for c in constants]
    print(tbls.format_pretty_table(data, column_names=["Const", "Index"]))


def draw_ids_table(ids):
    print("ID")
    data = [[c.value, c.typeName, c.index] for c in ids]
    print(tbls.format_pretty_table(data, column_names=["Const", "Type", "Index"]))
