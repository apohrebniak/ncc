class PrecedenceTableBuilder:
  things = set()
  grammar = [
    ['$program', 'id', '$block'],
    ['$block', '{', '$stmts1', '}'],
    ['$stmts1', '$stmts'],
    ['$block', '{', '}'],
    ['$stmts', '$stmt'],
    ['$stmts', '$stmt', '\\n', '$stmts'],
    ['$stmt', '$block'],
    ['$stmt', 'if', '$log.expr1', '?', '$block', ':', '$block'],
    ['$log.expr1', '$log.expr'],
    ['$stmt', 'while', '$log.expr1', 'do', '$block'],
    ['$stmt', 'int', 'id'],
    ['$stmt', 'int', 'id', '=', '$expr1'],
    ['$expr1', '$expr'],
    ['$stmt', 'float', 'id'],
    ['$stmt', 'float', 'id', '=', '$expr1'],
    ['$stmt', 'id', '=', '$expr1'],
    ['$stmt', 'in', '(', '$args1', ')'],
    ['$args1', '$args'],
    ['$stmt', 'out', '(', '$args1', ')'],
    ['$expr', '$term1'],
    ['$expr', '$expr', '+', '$term1'],
    ['$expr', '$expr', '-', '$term1'],
    ['$expr', '-', '$term1'],
    ['$term1', '$term'],
    ['$term', '$factor1'],
    ['$factor1', '$factor'],
    ['$term', '$term', '*', '$factor'],
    ['$term', '$term', '/', '$factor'],
    ['$factor', '(', '$expr1', ')'],
    ['$factor', 'id'],
    ['$factor', 'const'],
    ['$log.expr', '$log.term1'],
    ['$log.expr', '$log.expr', 'or', '$log.term1'],
    ['$log.term1', '$log.term'],
    ['$log.term', '$log.factor'],
    ['$log.term', '$log.term', 'and', '$log.factor'],
    ['$log.factor', '[', '$log.expr1', ']'],
    ['$log.factor', 'not', '$log.factor'],
    ['$log.factor', '$expr', '>', '$expr1'],
    ['$log.factor', '$expr', '>=', '$expr1'],
    ['$log.factor', '$expr', '<', '$expr1'],
    ['$log.factor', '$expr', '<=', '$expr1'],
    ['$log.factor', '$expr', '==', '$expr1'],
    ['$log.factor', '$expr', '!=', '$expr1'],
    ['$args', '$args', ',', 'id'],
    ['$args', ',', 'id']
  ]
  table = []
  equal_pairs2 = []
  equal_pairs3 = []
  equal_pairs3b = []
  exception_pair = ()

  def process(self):
    try:
      self.create_table()
      self.fill_equals()
      self.fill_less()
      self.fill_greater()
      self.fill_greater_additional()
      print(self.prepare_table())
    except:
      print("КОНФЛИКТ! "
            "ПОПЫТКА ПОМЕНЯТЬ ЗНАК С " + self.exception_pair[2] + " "
                                                                  "НА " +
            self.exception_pair[3] + " "
                                     "МЕЖДУ " + self.exception_pair[0] + " И " +
            self.exception_pair[1] + "\n")

  def prepare_table(self):
    prepared_table = ""
    first_row = True
    row_count = 0
    for row in self.table:
      prepared_table += '|'
      if first_row:
        prepared_table += '{:30}'.format('1 \ 2') + '|'
        i = 1
        while i < row.__len__():
          prepared_table += '{:3}'.format(str(i)) + '|'
          i = i + 1
      else:
        first_thing = True
        for thing in row:
          if first_thing:
            if thing[0] == '$':
              thing = thing[1:]
            prepared_table += '№' + '{:3}'.format(
              str(row_count)) + '{:25}'.format(str(thing)) + '|'
          else:
            prepared_table += '{:3}'.format(str(thing)) + '|'
          if first_thing:
            first_thing = False
      if first_row:
        first_row = False
      prepared_table += '\n'
      row_count = row_count + 1
    print("FIRST+\n")
    for thing in self.things:
      if thing[0] == '$':
        print(thing + ": " + str(self.find_first_plus(thing)) + "\n")
    print("\nLAST+\n")
    for thing in self.things:
      if thing[0] == '$':
        print(thing + ": " + str(self.find_last_plus(thing)) + "\n")
    return prepared_table

  def create_table(self):
    things = set()
    for sentence in self.grammar:
      for thing in sentence:
        things.add(thing)
    things.remove('$program')
    self.things = list(things)
    self.table.append(['1 \ 2'])
    for thing in self.things:
      self.table[0].append(thing)
    things_length = self.things.__len__()
    self.table[0].append('#')
    empty_space = []
    i = 0
    while i < things_length:
      empty_space.append('')
      i = i + 1
    empty_space.append('>')
    less_space = []
    i = 0
    while i < things_length:
      less_space.append('<')
      i = i + 1
    i = 0
    while i < things_length:
      self.table.append([self.things[i]] + empty_space)
      i = i + 1
    self.table.append(['#'] + less_space + [''])

  def fill_equals(self):
    for sentence in self.grammar:
      index = 1
      while index < sentence.__len__() - 1:
        first = sentence[index]
        second = sentence[index + 1]
        if first[0] == '$' and second[0] == '$':
          self.equal_pairs3b.append((first, second))
        else:
          if first[0] == '$':
            self.equal_pairs3.append((first, second))
          else:
            if second[0] == '$':
              self.equal_pairs2.append((first, second))
        self.table_write(first, second, '=')
        index = index + 1

  def fill_less(self):
    for pair in self.equal_pairs2:
      first_plus = self.find_first_plus(pair[1])
      for thing in first_plus:
        self.table_write(pair[0], thing, '<')

  def fill_greater(self):
    for pair in self.equal_pairs3:
      last_plus = self.find_last_plus(pair[0])
      if pair[1][0] != '$':
        for thing in last_plus:
          self.table_write(thing, pair[1], '>')
      else:
        first_plus = self.find_first_plus(pair[1])
        for thing1 in last_plus:
          for thing2 in first_plus:
            self.table_write(thing1, thing2, '>')

  def fill_greater_additional(self):
    for pair in self.equal_pairs3b:
      last_plus = self.find_last_plus(pair[0])
      first_plus = self.find_first_plus(pair[1])
      for thing1 in last_plus:
        for thing2 in first_plus:
          self.table_write(thing1, thing2, '>')

  def table_write(self, row_thing, col_thing, sign):
    row = self.get_index(row_thing)
    col = self.get_index(col_thing)
    if self.table[row][col] == '':
      self.table[row][col] = sign
    else:
      if not (self.table[row][col] == sign):
        self.exception_pair = (row_thing, col_thing, self.table[row][col], sign)
        raise Exception

  def get_index(self, thing):
    i = 0
    for th in self.things:
      i = i + 1
      if th == thing:
        break
    return i

  def find_first_plus(self, thing):
    if thing[0] == '$':
      first_plus = set()
      for sentence in self.grammar:
        if sentence[0] == thing:
          first_plus.add(sentence[1])
          if sentence[1] != sentence[0]:
            if sentence[1][0] == '$':
              first_plus = first_plus.union(self.find_first_plus(sentence[1]))
      return list(first_plus)
    return []

  def find_last_plus(self, thing):
    if thing[0] == '$':
      last_plus = set()
      for sentence in self.grammar:
        if sentence[0] == thing:
          last_plus.add(sentence[sentence.__len__() - 1])
          if sentence[sentence.__len__() - 1] != sentence[0]:
            if sentence[sentence.__len__() - 1][0] == '$':
              last_plus = last_plus.union(
                self.find_last_plus(sentence[sentence.__len__() - 1]))
      return list(last_plus)
    return []


builder = PrecedenceTableBuilder()
builder.process()
