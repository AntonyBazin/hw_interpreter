from parser import Parser, STNode


class Descriptor:
    """Used for describing a variable in a dictionary"""

    def __init__(self, dtype, value):
        self.type = dtype
        self.value = value

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

    def interpret(self, code: str):
        t = self.parser.parse(code)
        STNode.paste(t, 0)
        try:
            print(self._interpret_node(t))
        except RedeclarationError as er:
            print(er.__doc__)
        except NotFoundError as nf:
            print(nf.__doc__)
        print(self.nmsp_stack)
        self.nmsp_stack = []  # for debug

    def _interpret_node(self, node: STNode):
        if node is None:
            return
        elif node.type == 'program':
            self.nmsp_stack.append({})
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
        elif node.type == 'id':
            return node.parts[0].value
        elif node.type == 'invert':
            return -self._interpret_node(node.parts[0])
        elif node.type == 'conjunction':
            self._interpret_node(node.parts[0])
            return self._interpret_node(node.parts[1])
        elif node.type == 'create':
            ldt = self.nmsp_stack.pop()
            if node.parts[0].value in ldt.keys():
                raise RedeclarationError
            ldt[node.parts[0].value] = Descriptor(node.parts[0].type, node.parts[1].value)
            node.parts[0].add_part(node.parts[1])
            self.nmsp_stack.append(ldt)
            return self._interpret_node(node.parts[0])
        elif node.type == 'assign':
            self._interpret_node(node.parts[0]).parts[0] = node.parts[1].value
            return node.parts[0].parts[0].value
        elif node.type == 'call':
            ldt = self.nmsp_stack.pop()
            if node.value not in ldt.keys():
                self.nmsp_stack.append(ldt)
                raise NotFoundError
            self.nmsp_stack.append(ldt)
            return ldt[node.value].value


if __name__ == '__main__':
    interpreter = Interpreter()
    while True:
        interpreter.interpret(input())
