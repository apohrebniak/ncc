class Table:

    def __init__(self, columns):
        self.columns = columns
        self.rows = []

    def add_row(self, *row):
        assert len(row) == self.columns
        self.rows.append(row)
        return len(self.rows)

    def contains(self, value, column):
        return True if len([row for row in self.rows if row[column] == value]) else False

    def next_index(self):
        return len(self.rows)

    def get_row_for_value(self, value, column):
        l = [row for row in self.rows if row[column] == value]
        if len(l) > 0:
            return l[0]
        else:
            return None

    def __str__(self):
        return self.rows.__str__()
