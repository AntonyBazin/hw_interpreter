from parser import Parser, STNode


class Interpreter:
    def __init__(self):
        self.parser = Parser()

    def interpret(self, code: str):
        t = self.parser.parse(code)
        STNode.paste(t, 0)
        print(self._interpret_node(t))

    def _interpret_node(self, node: STNode):
        if node is None:
            return
        elif node.type == 'program':
            return self._interpret_node(node.parts[0])
        elif node.type == 'number':
            return node.value
        elif node.type == 'oper':
            if node.value == '+':
                return self._interpret_node(node.parts[0])\
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
            return node.value
        elif node.type == 'invert':
            return -self._interpret_node(node.parts[0])
        elif node.type == 'conjunction':
            return None
        elif node.type == 'create':
            return self._interpret_node(node.parts[0])


if __name__ == '__main__':
    interpreter = Interpreter()
    while True:
        interpreter.interpret(input())
