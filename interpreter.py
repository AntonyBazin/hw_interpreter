from parser import Parser, STNode


class InterpreterException(Exception):
    pass


class RedeclarationError(InterpreterException):
    """Variable redeclaration error"""


class NotFoundError(InterpreterException):
    """Name not found error"""


class ConstAssignment(InterpreterException):
    """Constant assignment attempt"""


class ConstIncrement(InterpreterException):
    """Constant increment attempt"""


class ConstDecrement(InterpreterException):
    """Constant decrement attempt"""


class BoolIncrement(InterpreterException):
    """Bool increment attempt"""


class BoolDecrement(InterpreterException):
    """Bool decrement attempt"""


class BadBoolAssignment(InterpreterException):
    """Inappropriate value on bool assignment"""


class NegativeExtension(InterpreterException):  # TODO show the result
    """Negative value in expression for extending an array"""


class InvalidArrayOperator(InterpreterException):
    """Invalid operand for array operator"""


class Descriptor:
    """Used for describing a variable in a dictionary"""

    def __init__(self, dtype, value, node):
        self.type = dtype
        self.value = value
        self.link = node

    def __repr__(self):
        return str("(type {}, value: {})".format(str(self.type), str(self.value)))


class Interpreter:
    def __init__(self):
        self.parser = Parser()
        self.nmsp_stack = []
        self.LDT = {}

    def interpret(self, code: str):
        t = self.parser.parse(code)
        STNode.paste(t, 0)
        try:
            print(self._int_nd(t))
        # except InterpreterException as ie:
        #     print(ie.__doc__)
        except IndexError as ie:
            print(ie)
        print(self.nmsp_stack)
        print(self.LDT)
        # self.nmsp_stack = []  # for debug with many iterations
        # self.LDT = {}

    def create_vars(self, nodes):  # used in functions
        for node in nodes:
            self._int_nd(node)

    def asgn_args(self, dst, src):
        for i in range(len(dst)):
            if src[i]:
                if dst[i].type == 'create_id':
                    self._int_nd(STNode('assign', None, dst[i].parts[0], STNode('number', src[i])))
                elif dst[i].type == 'create_1darr':
                    dst[i].parts = [dst[i].parts[0]]
                    dst[i].parts.extend([STNode('number', j) for j in src[i]])
                    del self.LDT[dst[i].parts[0].value]
                    self._int_nd(dst[i])
                    self.LDT[dst[i].parts[0].value].value.reverse()
                elif dst[i].type == 'create_2darr':
                    dst[i].parts = [dst[i].parts[0]]
                    for j in src[i][::-1]:  # j -- inner lists
                        dst[i].parts.extend([STNode('enum', [STNode('number', k) for k in j[::-1]])])
                    del self.LDT[dst[i].parts[0].value]
                    self._int_nd(dst[i])
                    # self.LDT[dst[i].parts[0].value].value.reverse()
                    # for j in self.LDT[dst[i].parts[0].value].value:
                    #     j.reverse()
        return 0

    def parse_args(self, args):
        res = []
        for i in args:
            if i.type != 'empty_slot':
                if i.type == 'id':
                    res.append(self.LDT[i.value].value)
                else:
                    res.append(self._int_nd(i))
            else:
                res.append(None)
        return res

    def collect_rets(self, src):
        res = []
        for i in src:
            res.append(self.LDT[i.parts[0].value].value)
        return res

    def asgn_rets(self, dst, src):
        for i in range(len(dst)):
            if dst[i].type != 'empty_slot':
                if dst[i].type == 'id':
                    self._int_nd(STNode('assign', None, dst[i], STNode('number', src[i])))
                    # self.LDT[dst[i].value].value = src[i]
                elif dst[i].type == 'index_1d':  # TODO
                    self._int_nd(STNode('assign', None, dst[i].parts[0], dst[i].parts[1], STNode('number', src[i])))
                elif dst[i].type == 'index_2d':
                    self._int_nd(STNode('assign', None,
                                        dst[i].parts[0],
                                        dst[i].parts[1],
                                        dst[i].parts[2],
                                        STNode('number',
                                        src[i])))

    def _int_nd(self, node: STNode):
        if node is None:
            return

        elif node.type == 'program':
            if not self.nmsp_stack:
                self.nmsp_stack.append(self.LDT)
            return self._int_nd(node.parts[0])

        elif node.type == 'number':
            return node.value

        elif node.type == 'oper':
            if node.value == '+':
                return self._int_nd(node.parts[0]) \
                       + self._int_nd(node.parts[1])
            elif node.value == '-':
                return self._int_nd(node.parts[0]) \
                       - self._int_nd(node.parts[1])
            elif node.value == '*':
                return self._int_nd(node.parts[0]) \
                       * self._int_nd(node.parts[1])
            elif node.value == '/':
                return self._int_nd(node.parts[0]) \
                       // self._int_nd(node.parts[1])
            elif node.value == 'OR':
                return self._int_nd(node.parts[0]) \
                       and self._int_nd(node.parts[1])
            elif node.value == 'GT':
                return self._int_nd(node.parts[0]) \
                       > self._int_nd(node.parts[1])
            elif node.value == 'LT':
                return self._int_nd(node.parts[0]) \
                       < self._int_nd(node.parts[1])
            elif node.value == 'EQ':
                return self._int_nd(node.parts[0]) \
                       == self._int_nd(node.parts[1])

        elif node.type == 'id':
            if node.value not in self.LDT.keys():
                raise NotFoundError
            return self.LDT[node.value].value

        elif node.type == 'unary':
            if node.value == '-':
                return -node.parts[0].value

            elif node.value == 'NOT':
                return int(not self._int_nd(node.parts[0]))

            elif node.value == 'INC':
                if node.parts[0].value not in self.LDT.keys():
                    raise NotFoundError
                if self.LDT[node.parts[0].value].type in ('CUINT', 'CBOOL'):
                    raise ConstIncrement
                if self.LDT[node.parts[0].value].type == 'BOOL':
                    raise BoolIncrement
                self.LDT[node.parts[0].value].value += 1
                return self._int_nd(node.parts[0])

            elif node.value == 'DEC':
                if node.parts[0].value not in self.LDT.keys():
                    raise NotFoundError
                if self.LDT[node.parts[0].value].type in ('CUINT', 'CBOOL'):
                    raise ConstDecrement
                if self.LDT[node.parts[0].value].type == 'BOOL':
                    raise BoolDecrement
                self.LDT[node.parts[0].value].value -= 1
                return self._int_nd(node.parts[0])

        elif node.type == 'conjunction':
            self._int_nd(node.parts[0])
            return self._int_nd(node.parts[1])

        elif node.type == 'create_id':
            if node.parts[0].value in self.LDT.keys():
                raise RedeclarationError
            if node.value in ('UINT', 'CUINT'):
                self.LDT[node.parts[0].value] = Descriptor(node.value,
                                                           self._int_nd(node.parts[1]),
                                                           node.parts[0])
            elif node.value in ('BOOL', 'CBOOL'):
                res = self._int_nd(node.parts[1])
                if res in (0, 1):
                    self.LDT[node.parts[0].value] = Descriptor(node.value,
                                                               res,
                                                               node.parts[0])
                else:
                    raise BadBoolAssignment
            return self.LDT[node.parts[0].value].value

        elif node.type == 'assign':
            if node.parts[0].value not in self.LDT.keys():
                raise NotFoundError
            if self.LDT[node.parts[0].value].type in ('CUINT', 'CBOOL'):
                raise ConstAssignment
            elif self.LDT[node.parts[0].value].type == 'BOOL':
                res = self._int_nd(node.parts[1])
                if res in (0, 1):
                    self.LDT[node.parts[0].value].value = res
                else:
                    raise BadBoolAssignment
                return self.LDT[node.parts[0].value].value
            elif self.LDT[node.parts[0].value].type == 'UINT':
                self.LDT[node.parts[0].value].value = self._int_nd(node.parts[1])
                return self.LDT[node.parts[0].value].value
            elif self.LDT[node.parts[0].value].type == '1DARRINT':
                self.LDT[node.parts[0].value].value[self._int_nd(node.parts[1])] \
                    = self._int_nd(node.parts[2])
                return self.LDT[node.parts[0].value].value[self._int_nd(node.parts[1])]
            elif self.LDT[node.parts[0].value].type == '1DARRBOOL':
                res = self._int_nd(node.parts[2])
                if res in (0, 1):
                    self.LDT[node.parts[0].value].value[self._int_nd(node.parts[1])] = res
                else:
                    raise BadBoolAssignment
                return self.LDT[node.parts[0].value].value[self._int_nd(node.parts[1])]
            elif self.LDT[node.parts[0].value].type == '2DARRINT':
                self.LDT[node.parts[0].value].value[self._int_nd(node.parts[1])][self._int_nd(node.parts[2])] \
                    = self._int_nd(node.parts[3])
            else:
                res = self._int_nd(node.parts[2])
                if res in (0, 1):
                    self.LDT[node.parts[0].value].value[self._int_nd(node.parts[1])][self._int_nd(node.parts[2])] \
                        = res
                else:
                    raise BadBoolAssignment

        elif node.type == 'if':
            if len(node.parts) == 2:
                if self._int_nd(node.parts[0]):
                    self._int_nd(node.parts[1])
            else:
                if self._int_nd(node.parts[0]):
                    self._int_nd(node.parts[1])
                else:
                    self._int_nd(node.parts[2])

        elif node.type == 'while':
            while self._int_nd(node.parts[0]):
                self._int_nd(node.parts[1])

        elif node.type == 'create_1darr':
            if node.parts[0].value in self.LDT.keys():
                raise RedeclarationError
            self.LDT[node.parts[0].value] = Descriptor(node.value, [], None)
            if node.value == '1DARRBOOL':
                for i in node.parts[1:]:
                    res = self._int_nd(i)
                    if res in (0, 1):
                        self.LDT[node.parts[0].value].value.append(res)
                    else:
                        del self.LDT[node.parts[0].value]
                        raise BadBoolAssignment
            else:
                self.LDT[node.parts[0].value].value = [self._int_nd(i) for i in node.parts[1:]]
            self.LDT[node.parts[0].value].value.reverse()

        elif node.type == 'index_1d':
            if node.parts[0].value not in self.LDT.keys():
                raise NotFoundError
            return self.LDT[node.parts[0].value].value[self._int_nd(node.parts[1])]

        elif node.type == 'index_2d':
            if node.parts[0].value not in self.LDT.keys():
                raise NotFoundError
            res = self.LDT[node.parts[0].value].value[self._int_nd(node.parts[1])][self._int_nd(node.parts[2])]
            return res

        elif node.type == 'size_1d':
            if node.parts[0].value not in self.LDT.keys():
                raise NotFoundError
            return len(self.LDT[node.parts[0].value].value)

        elif node.type == 'size_2d':
            if node.parts[0].value not in self.LDT.keys():
                raise NotFoundError
            return len(self.LDT[node.parts[0].value].value[self._int_nd(node.parts[1])])

        elif node.type == 'extend1':
            if node.parts[0].value not in self.LDT.keys():
                raise NotFoundError
            if self.LDT[node.parts[0].value].type in ('1DARRINT', '1DARRBOOL'):
                if self._int_nd(node.parts[1]) < 0:
                    raise NegativeExtension
                extension = [0 for _ in range(self._int_nd(node.parts[1]))]
                self.LDT[node.parts[0].value].value.extend(extension)
            elif self.LDT[node.parts[0].value].type in ('2DARRBOOL', '2DARRINT'):
                ext_ln = self._int_nd(node.parts[1])
                int_ln = len(self.LDT[node.parts[0].value].value[-1])
                if ext_ln < 0:
                    raise NegativeExtension
                extension = [[0 for _ in range(int_ln)] for _ in range(ext_ln)]
                self.LDT[node.parts[0].value].value.extend(extension)
            else:
                raise InvalidArrayOperator

        elif node.type == 'create_2darr':
            if node.parts[0].value in self.LDT.keys():
                raise RedeclarationError
            self.LDT[node.parts[0].value] = Descriptor(node.value, [[]], None)
            if node.value == '2DARRBOOL':
                for i in range(1, len(node.parts)):
                    node.parts[i].value.reverse()
                    for j in node.parts[i]:
                        if j not in (0, 1):
                            raise BadBoolAssignment

            self.LDT[node.parts[0].value].value = list(map(lambda x: list(map(self._int_nd, x.value)), node.parts[1:]))
            for i in self.LDT[node.parts[0].value].value:
                i.reverse()
            self.LDT[node.parts[0].value].value.reverse()

        elif node.type == 'extend2':
            if node.parts[0].value not in self.LDT.keys():
                raise NotFoundError
            if self.LDT[node.parts[0].value].type in ('2DARRBOOL', '2DARRINT'):
                index = self._int_nd(node.parts[1])
                ext_len = self._int_nd(node.parts[2])
                if ext_len < 0:
                    raise NegativeExtension
                extension = [0 for _ in range(ext_len)]
                self.LDT[node.parts[0].value].value[index].extend(extension)
            else:
                raise InvalidArrayOperator

        elif node.type == 'declare':
            if node.parts[0].value in self.LDT.keys():
                raise RedeclarationError
            node.parts[-1].value.reverse()
            node.parts[-2].value.reverse()
            self.LDT[node.parts[0].value] = Descriptor(node.value,
                                                       None,
                                                       node)

        elif node.type == 'call':
            if node.value.value not in self.LDT.keys():
                raise NotFoundError
            fptr = self.LDT[node.value.value].link  # link to the function declaration
            node.parts[0].value.reverse()  # reverse the args' lists
            node.parts[1].value.reverse()
            args = self.parse_args(node.parts[1].value)
            self.nmsp_stack.append(self.LDT)
            self.LDT = {}
            try:
                self.create_vars(fptr.parts[-1].value)  # create parameters and return values inside the function
                self.create_vars(fptr.parts[-2].value)
                self.asgn_args(fptr.parts[-1].value, args)
            except BadBoolAssignment as bd:
                self.LDT = self.nmsp_stack.pop()  # restore LDT: pop from stack
                raise
            self._int_nd(fptr.parts[1])  # execute body
            ret_values = self.collect_rets(fptr.parts[-2].value)  # TODO
            self.LDT = self.nmsp_stack.pop()
            self.asgn_rets(node.parts[0].value, ret_values)  # assign ret-values
            return None


if __name__ == '__main__':
    interpreter = Interpreter()
    # choice = input()
    # if choice == '1':
    while True:
        interpreter.interpret(input())
    # else:
    #     with open('examples', 'r') as f:
    #         choice = f.read()
    #     interpreter.interpret(choice)
