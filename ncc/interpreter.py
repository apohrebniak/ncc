import sys

import ncc.common as cmn
import ncc.rpn_token as rpntoken

TYPE_INT, TYPE_FLOAT = range(2)


class Constant:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Identity:
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value


class Label:
    def __init__(self, index, offset):
        self.index = index
        self.offset = offset


class Bool:
    def __init__(self, value):
        self.value = value


class Count:
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(self, rpn_tokens):
        self.tokens = rpn_tokens
        self.stack = []
        self._lexeme_function_map = self._build_lexeme_function_map()
        self.curr_index = 0
        self.identity_map = dict()

    def run(self):
        while self.curr_index < len(self.tokens):
            token = self.tokens[self.curr_index]
            if isinstance(token, rpntoken.RPNConstant):

                tp = TYPE_FLOAT if type(token.lexeme) == float else TYPE_INT
                v = token.lexeme
                self.stack.append(Constant(type=tp, value=v))

            elif isinstance(token, rpntoken.RPNIdentity):

                identity = self.identity_map[
                    token.lexeme] if token.lexeme in self.identity_map.keys() else Identity(
                    name=token.lexeme, type=None, value=None)
                self.stack.append(identity)

            elif isinstance(token, rpntoken.RPNLabel):

                self.stack.append(
                    Label(index=token.index, offset=token.offset))

            elif isinstance(token, rpntoken.RPNArgsCountToken):

                self.stack.append(Count(value=token.count))

            else:
                self._lexeme_function_map[token.rtag]()

            self.curr_index += 1

    def _build_lexeme_function_map(self):
        return {
            cmn.R_INT: self._op_int,
            cmn.R_FLOAT: self._op_float,
            cmn.R_ASSGN: self._op_assign,
            cmn.R_PLUS: self._op_plus,
            cmn.R_MINUS: self._op_minus,
            cmn.R_MUL: self._op_mul,
            cmn.R_DIV: self._op_div,
            cmn.R_OR: self._op_or,
            cmn.R_AND: self._op_and,
            cmn.R_NOT: self._op_not,
            cmn.R_HI: self._op_hi,
            cmn.R_LOW: self._op_low,
            cmn.R_EQ: self._op_eq,
            cmn.R_NEQ: self._op_neq,
            cmn.R_HIEQ: self._op_hieq,
            cmn.R_LOWEQ: self._op_loweq,
            cmn.R_UNARY_MINUS: self._op_unary_minus,
            cmn.R_IN: self._op_in,
            cmn.R_OUT: self._op_out,
            cmn.R_JMPF: self._op_jmpf,
            cmn.R_JMP: self._op_jmp,
        }

    def _op_int(self):
        id = self.stack.pop()

        if not isinstance(id, Identity):
            raise Exception

        if id.name in self.identity_map.keys():
            raise Exception
        else:
            id.value = int(0)
            id.type = TYPE_INT
            self.identity_map[id.name] = id
            self.stack.append(id)

    def _op_float(self):
        id = self.stack.pop()

        if not isinstance(id, Identity):
            raise Exception

        if id.name in self.identity_map.keys():
            raise Exception
        else:
            id.value = float(0)
            id.type = TYPE_FLOAT
            self.identity_map[id.name] = id
            self.stack.append(id)

    def _op_assign(self):
        r_value = self.stack.pop()
        l_value = self.stack.pop()

        payload = r_value.value
        l_value.value = int(payload) if l_value.type == TYPE_INT else float(
            payload)

        self.stack.append(l_value)

    def _op_plus(self):
        r_value = self.stack.pop()
        l_value = self.stack.pop()

        r_payload = r_value.value
        l_payload = l_value.value

        result_payload = l_payload + r_payload

        if r_value.type == TYPE_FLOAT or l_value.type == TYPE_FLOAT:
            result_payload = float(result_payload)

        tp = TYPE_FLOAT if type(result_payload) == float else TYPE_INT

        self.stack.append(Constant(type=tp, value=result_payload))

    def _op_minus(self):
        r_value = self.stack.pop()
        l_value = self.stack.pop()

        r_payload = r_value.value
        l_payload = l_value.value

        result_payload = l_payload - r_payload

        if r_value.type == TYPE_FLOAT or l_value.type == TYPE_FLOAT:
            result_payload = float(result_payload)

        tp = TYPE_FLOAT if type(result_payload) == float else TYPE_INT

        self.stack.append(Constant(type=tp, value=result_payload))

    def _op_mul(self):
        r_value = self.stack.pop()
        l_value = self.stack.pop()

        r_payload = r_value.value
        l_payload = l_value.value

        result_payload = l_payload * r_payload

        if r_value.type == TYPE_FLOAT or l_value.type == TYPE_FLOAT:
            result_payload = float(result_payload)

        tp = TYPE_FLOAT if type(result_payload) == float else TYPE_INT

        self.stack.append(Constant(type=tp, value=result_payload))

    def _op_div(self):  # TODO: division by 0
        r_value = self.stack.pop()
        l_value = self.stack.pop()

        r_payload = r_value.value
        l_payload = l_value.value

        try:
            result_payload = l_payload / r_payload
        except ZeroDivisionError:
            print("Division by zero!", file=sys.stderr)
            sys.exit(1)

        if r_value.type == TYPE_FLOAT or l_value.type == TYPE_FLOAT:
            result_payload = float(result_payload)

        tp = TYPE_FLOAT if type(result_payload) == float else TYPE_INT

        self.stack.append(Constant(type=tp, value=result_payload))

    def _op_or(self):
        r_value = self.stack.pop()
        l_value = self.stack.pop()

        r_payload = r_value.value
        l_payload = l_value.value

        result_payload = l_payload or r_payload

        self.stack.append(Bool(value=result_payload))

    def _op_and(self):
        r_value = self.stack.pop()
        l_value = self.stack.pop()

        r_payload = r_value.value
        l_payload = l_value.value

        result_payload = l_payload and r_payload

        self.stack.append(Bool(value=result_payload))

    def _op_not(self):
        stack_value = self.stack.pop()

        payload = stack_value.value

        result_payload = not payload

        self.stack.append(Bool(value=result_payload))

    def _op_hi(self):
        r_value = self.stack.pop()
        l_value = self.stack.pop()

        r_payload = r_value.value
        l_payload = l_value.value

        result_payload = l_payload > r_payload

        self.stack.append(Bool(value=result_payload))

    def _op_low(self):
        r_value = self.stack.pop()
        l_value = self.stack.pop()

        r_payload = r_value.value
        l_payload = l_value.value

        result_payload = l_payload < r_payload

        self.stack.append(Bool(value=result_payload))

    def _op_eq(self):
        r_value = self.stack.pop()
        l_value = self.stack.pop()

        r_payload = r_value.value
        l_payload = l_value.value

        result_payload = l_payload == r_payload

        self.stack.append(Bool(value=result_payload))

    def _op_neq(self):
        r_value = self.stack.pop()
        l_value = self.stack.pop()

        r_payload = r_value.value
        l_payload = l_value.value

        result_payload = l_payload != r_payload

        self.stack.append(Bool(value=result_payload))

    def _op_hieq(self):
        r_value = self.stack.pop()
        l_value = self.stack.pop()

        r_payload = r_value.value
        l_payload = l_value.value

        result_payload = l_payload >= r_payload

        self.stack.append(Bool(value=result_payload))

    def _op_loweq(self):
        r_value = self.stack.pop()
        l_value = self.stack.pop()

        r_payload = r_value.value
        l_payload = l_value.value

        result_payload = l_payload <= r_payload

        self.stack.append(Bool(value=result_payload))

    def _op_unary_minus(self):
        stack_value = self.stack.pop()

        payload = stack_value.value

        result_payload = - payload

        t = TYPE_FLOAT if type(stack_value) == float else TYPE_INT

        self.stack.append(Constant(type=t, value=result_payload))

    def _op_in(self):
        value_count = self.stack.pop()
        count = value_count.value

        args = []
        while count != 0:
            args.insert(0, self.stack.pop())
            count -= 1

        for arg in args:
            input_string = input("{} <- ".format(arg.name))
            try:
                arg.value = int(
                    input_string) if arg.type == TYPE_INT else float(
                    input_string)
            except Exception:
                print("Error while parsing input string '{}'!".format(
                    input_string), file=sys.stderr)
                sys.exit(1)

    def _op_out(self):
        value_count = self.stack.pop()
        count = value_count.value

        args = []
        while count != 0:
            args.insert(0, self.stack.pop())
            count -= 1

        for arg in args:
            print("{} -> {}".format(arg.name, arg.value))

    def _op_jmpf(self):
        r_value_label = self.stack.pop()
        l_value_logic = self.stack.pop()

        l_payload_logic = l_value_logic.value

        if not l_payload_logic:
            self.curr_index = r_value_label.offset

    def _op_jmp(self):
        stack_value_label = self.stack.pop()

        self.curr_index = stack_value_label.offset
