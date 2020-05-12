from parser import Parser, STNode


class Descriptor:
    """Used for describing a variable in a dictionary"""

    def __init__(self, dtype, value, node):
        self.type = dtype
        self.value = value
        self.link = node

    def __repr__(self):
        return str("(type {}, value: {})".format(str(self.type), str(self.value)))


class RedeclarationError(Exception):
    """Variable redeclaration error"""


class NotFoundError(Exception):
    """Name not found error"""


class Interpreter:
    def __init__(self):
        self.parser = Parser()
        self.nmsp_stack = []
        self.LDT = {}

    def interpret(self, code: str):
        t = self.parser.parse(code)
        STNode.paste(t, 0)
        try:
            print(self._interpret_node(t))
        except RedeclarationError as er:
            print(er.__doc__)
            raise
        except NotFoundError as nf:
            print(nf.__doc__)
        print(self.nmsp_stack)
        self.nmsp_stack = []  # for debug
        self.LDT = {}

    def _interpret_node(self, node: STNode):
        if node is None:
            return
        elif node.type == 'program':
            self.nmsp_stack.append(self.LDT)
            return self._interpret_node(node.parts[0])
        elif node.type == 'number':
            return node.value
        elif node.type == 'oper':
            if node.value == '+':
                return self._interpret_node(node.parts[0]) \
                       + self._interpret_node(node.parts[1])
            elif node.value == '-':
                return self._interpret_node(node.parts[0]) \
                       - self._interpret_node(node.parts[1])
            elif node.value == '*':
                return self._interpret_node(node.parts[0]) \
                       * self._interpret_node(node.parts[1])
            elif node.value == '/':
                return self._interpret_node(node.parts[0]) \
                       // self._interpret_node(node.parts[1])
            elif node.value == 'OR':
                return self._interpret_node(node.parts[0]) \
                       and self._interpret_node(node.parts[1])
            elif node.value == 'GT':
                return self._interpret_node(node.parts[0]) \
                       > self._interpret_node(node.parts[1])
            elif node.value == 'LT':
                return self._interpret_node(node.parts[0]) \
                       < self._interpret_node(node.parts[1])
            elif node.value == 'EQ':
                return self._interpret_node(node.parts[0]) \
                       == self._interpret_node(node.parts[1])
        elif node.type == 'id':
            if node.value not in self.LDT.keys():
                raise NotFoundError
            return self.LDT[node.value].value
        elif node.type == 'unary':
            if node.value == '-':
                return -node.parts[0].value
            elif node.value == 'NOT':
                return int(not self._interpret_node(node.parts[0]))
            elif node.value == 'INC':
                if node.parts[0].value not in self.LDT.keys():
                    raise NotFoundError
                self.LDT[node.parts[0].value].value += 1
                return self._interpret_node(node.parts[0])
            elif node.value == 'DEC':
                if node.parts[0].value not in self.LDT.keys():
                    raise NotFoundError
                self.LDT[node.parts[0].value].value -= 1
                return self._interpret_node(node.parts[0])
        elif node.type == 'conjunction':
            self._interpret_node(node.parts[0])
            return self._interpret_node(node.parts[1])
        elif node.type == 'create':
            if node.parts[0].value in self.LDT.keys():
                raise RedeclarationError
            self.LDT[node.parts[0].value] = Descriptor(node.parts[0].type,
                                                       self._interpret_node(node.parts[1]),
                                                       node.parts[0])
            return self._interpret_node(node.parts[0])
        elif node.type == 'assign':
            self.LDT[node.parts[0].value].value = self._interpret_node(node.parts[1])
            return self.LDT[node.parts[0].value].value
        elif node.type == 'call':
            if node.value not in self.LDT.keys():
                raise NotFoundError
            return self.LDT[node.value].value
        elif node.type == 'if':
            if len(node.parts) == 2:
                if self._interpret_node(node.parts[0]):
                    self._interpret_node(node.parts[1])
            else:
                if self._interpret_node(node.parts[0]):
                    self._interpret_node(node.parts[1])
                else:
                    self._interpret_node(node.parts[2])
        elif node.type == 'while':
            while self._interpret_node(node.parts[0]):
                self._interpret_node(node.parts[1])


if __name__ == '__main__':
    interpreter = Interpreter()
    while True:
        interpreter.interpret(input())
