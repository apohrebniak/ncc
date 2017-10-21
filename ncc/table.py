class Table:
    def __init__(self):
        self.rows = dict()
        self.index = 0

    def contains_value(self, value):
        return value in self.rows

    def get_index_of_value(self, value):
        return self.rows[value].index


class Row:
    def __init__(self, value, index):
        self.value = value
        self.index = index


class ConstantTable(Table):
    def __init__(self):
        super().__init__()

    def add_and_get_index(self, value):
        if value not in self.rows:
            self.rows[value] = Row(value, self.index)
            self.index += 1
        return self.rows[value].index

    def __str__(self):
        result = "\t".join(["Value", "Index"])
        for row in self.rows.values():
            result += "\n{}\t{}".format(row.value, row.index)
        return result


class IndTable(Table):
    class IndRow(Row):
        def __init__(self, value, type_name, index):
            super().__init__(value, index)
            self.typeName = type_name

    def __init__(self):
        super().__init__()

    def add_and_get_idex(self, value, type_name):
        if value not in self.rows:
            self.rows[value] = self.IndRow(value, type_name, self.index)
            self.index += 1
        return self.rows[value].index

    def __str__(self):
        result = "\t".join(["Value", "Type", "Index"])
        for row in self.rows.values():
            result += "\n{}\t{}\t{}".format(row.value, row.typeName, row.index)
        return result
