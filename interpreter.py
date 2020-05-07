from parser import Parser, STNode


class Interpreter:
    def __init__(self):
        self.parser = Parser()

    def interpret(self, code: str):
        pass

    def _interpret_node(self, node: STNode):
        if node is None:
            return
        elif node.type == 'program':
            self._interpret_node(node.parts[0])
        elif node.type == 'number':
            return node.value
        elif node.type == 'oper':
            if node.value == 'PLUS':
                return self._interpret_node(node.parts[0])\
                       + self._interpret_node(node.parts[1])
            elif node.type == 'MINUS':
                return self._interpret_node(node.parts[0]) \
                       - self._interpret_node(node.parts[1])
            elif node.type == 'MUL':
                return self._interpret_node(node.parts[0]) \
                       * self._interpret_node(node.parts[1])
            elif node.type == 'DIV':
                return self._interpret_node(node.parts[0]) \
                       // self._interpret_node(node.parts[1])
        elif node.type == 'id':
            return node.value
        elif node.type == 'invert':
            return -self._interpret_node(node.parts[0])
        elif node.type == 'conjunction':
            return None

