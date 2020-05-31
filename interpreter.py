from parser import Parser, STNode
import sys


class InterpreterError(Exception):
    """Base Error Class"""

    def __init__(self, line):
        self.lineno = line

    def __str__(self):
        return self.__doc__ + ':' + str(self.lineno)


class RedeclarationError(InterpreterError):
    """Variable redeclaration error"""


class NotFoundError(InterpreterError):
    """Name not found error"""


class ConstAssignment(InterpreterError):
    """Constant assignment attempt"""


class ConstIncrement(InterpreterError):
    """Constant increment attempt"""


class ConstDecrement(InterpreterError):
    """Constant decrement attempt"""


class BoolIncrement(InterpreterError):
    """Bool increment attempt"""


class BoolDecrement(InterpreterError):
    """Bool decrement attempt"""


class BadBoolAssignment(InterpreterError):
    """Inappropriate value on bool assignment"""


class BadExtension(InterpreterError):
    """Negative or NoneType value in expression for extending an array"""


class InvalidArrayOperator(InterpreterError):
    """Invalid operand for array operator"""


class InvalidIndexingObject(InterpreterError):
    """Invalid variable for indexing"""


class RecursionStackOverflow(InterpreterError):
    """Too deep level of recursion"""


class NoneTypeError(InterpreterError):
    """Nonetype object at an important place"""


class ZeroDivError(InterpreterError):
    """Division by zero"""


class NoFieldError(InterpreterError):
    """Robot command used without a valid field loaded"""


class ExitFound(Exception):
    """Robot has found the exit at"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return self.__doc__ + '({0}, {1})!'.format(self.x, self.y)


class Descriptor:
    """Used for describing a variable in a dictionary"""

    def __init__(self, dtype, value, node):
        self.type = dtype
        self.value = value
        self.link = node

    def __repr__(self):
        return str("(type {}, value: {})".format(str(self.type), str(self.value)))


class Interpreter:
    def __init__(self, field=None, robot=None):
        self.parser = Parser()
        self.nmsp_stack = []
        self.LDT = {}
        self._errors = []
        self._functions = {}
        self.field = field
        self.robot = robot

    def interpret(self, code: str):
        t = self.parser.parse(code)
        if t is None:
            print('GGlobal syntax failure!')
            return
        if self.field is None:
            print('Field not acquired!')
        STNode.paste(t, 0)
        print(self._int_nd(t))
        print(self.LDT)
        print(self.robot)
        for e in self._errors:
            print(e)
        # self.nmsp_stack = []  # for debug with many iterations
        # self.LDT = {}

    def create_vars(self, nodes):  # used in functions
        for i in range(len(nodes)):
            self._int_nd(nodes[i])

    def asgn_args(self, dst, src):
        for i in range(len(dst)):
            if src[i]:
                if dst[i].type == 'create_id':
                    self._int_nd(STNode('assign', None, -1, dst[i].parts[0], STNode('number', src[i], -1)))
                elif dst[i].type == 'create_1darr':
                    dst[i].parts = [dst[i].parts[0]]
                    dst[i].parts.extend([STNode('number', j, -1) for j in src[i]])
                    del self.LDT[dst[i].parts[0].value]
                    self._int_nd(dst[i])
                    self.LDT[dst[i].parts[0].value].value.reverse()
                elif dst[i].type == 'create_2darr':
                    dst[i].parts = [dst[i].parts[0]]
                    for j in src[i][::-1]:  # j -- inner lists
                        dst[i].parts.extend([STNode('enum', [STNode('number', k, -1) for k in j[::-1]], -1)])
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
                    self._int_nd(STNode('assign', None, -1, dst[i], STNode('number', src[i], -1)))
                    # self.LDT[dst[i].value].value = src[i]
                elif dst[i].type == 'index_1d':
                    self._int_nd(
                        STNode('assign', None, -1, dst[i].parts[0], dst[i].parts[1], STNode('number', src[i], -1)))
                elif dst[i].type == 'index_2d':
                    self._int_nd(STNode('assign', None, -1,
                                        dst[i].parts[0],
                                        dst[i].parts[1],
                                        dst[i].parts[2],
                                        STNode('number', src[i], -1)))

    def _int_nd(self, node: STNode):
        if node is None:
            return

        elif node.type == 'program':
            if not self.nmsp_stack:
                self.nmsp_stack.append(self.LDT)
            return self._int_nd(node.parts[0])

        elif node.type == 'pass':
            return None

        elif node.type == 'number':
            return node.value

        elif node.type == 'oper':
            try:
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
                    try:
                        return self._int_nd(node.parts[0]) \
                               // self._int_nd(node.parts[1])
                    except ZeroDivisionError:
                        self._errors.append(ZeroDivError(node.lineno))
                        return self._int_nd(node.parts[0])
                elif node.value == 'OR':
                    return self._int_nd(node.parts[0]) \
                           or self._int_nd(node.parts[1])
                elif node.value == 'GT':
                    return self._int_nd(node.parts[0]) \
                           > self._int_nd(node.parts[1])
                elif node.value == 'LT':
                    return self._int_nd(node.parts[0]) \
                           < self._int_nd(node.parts[1])
                elif node.value == 'EQ':
                    return self._int_nd(node.parts[0]) \
                           == self._int_nd(node.parts[1])
            except TypeError as te:
                self._errors.append(te)
                return None

        elif node.type == 'id':
            if node.value not in self.LDT.keys():
                self._errors.append(NotFoundError(node.lineno))
                return None
            return self.LDT[node.value].value

        elif node.type == 'unary':
            if node.value == '-':
                return -node.parts[0].value

            elif node.value == 'NOT':
                try:
                    return int(not self._int_nd(node.parts[0]))
                except TypeError as te:
                    self._errors.append(te)
                    return None

            elif node.value == 'INC':
                if node.parts[0].value not in self.LDT.keys():
                    self._errors.append(NotFoundError(node.lineno))
                    return None
                try:
                    if self.LDT[node.parts[0].value].type in ('CUINT', 'CBOOL'):
                        self._errors.append(ConstIncrement(node.lineno))
                        return self._int_nd(node.parts[0])
                    if self.LDT[node.parts[0].value].type == 'BOOL':
                        self._errors.append(BoolIncrement(node.lineno))
                        return self._int_nd(node.parts[0])
                    self.LDT[node.parts[0].value].value += 1
                    return self._int_nd(node.parts[0])
                except TypeError as te:
                    self._errors.append(te)
                    return None

            elif node.value == 'DEC':
                if node.parts[0].value not in self.LDT.keys():
                    self._errors.append(NotFoundError(node.lineno))
                    return None
                try:
                    if self.LDT[node.parts[0].value].type in ('CUINT', 'CBOOL'):
                        self._errors.append(ConstDecrement(node.lineno))
                        return self._int_nd(node.parts[0])
                    if self.LDT[node.parts[0].value].type == 'BOOL':
                        self._errors.append(BoolDecrement(node.lineno))
                        return self._int_nd(node.parts[0])
                    self.LDT[node.parts[0].value].value -= 1
                    return self._int_nd(node.parts[0])
                except TypeError as te:
                    self._errors.append(te)
                    return None

        elif node.type == 'conjunction':
            self._int_nd(node.parts[0])
            self._int_nd(node.parts[1])

        elif node.type == 'create_id':
            if node.parts[0].value in self.LDT.keys():
                self._errors.append(RedeclarationError(node.lineno))
                return None
            if node.value in ('UINT', 'CUINT'):
                val = self._int_nd(node.parts[1])
                if val is not None:
                    self.LDT[node.parts[0].value] = Descriptor(node.value,
                                                               val,
                                                               node.parts[0])
                else:
                    self._errors.append(NoneTypeError(node.lineno))
                    return None
            elif node.value in ('BOOL', 'CBOOL'):
                res = self._int_nd(node.parts[1])
                if res in (0, 1):
                    self.LDT[node.parts[0].value] = Descriptor(node.value,
                                                               res,
                                                               node.parts[0])
                else:
                    self._errors.append(BadBoolAssignment(node.lineno))
                    self.LDT[node.parts[0].value] = Descriptor(node.value,
                                                               1,
                                                               node.parts[0])
            # return self.LDT[node.parts[0].value].value

        elif node.type == 'assign':
            if node.parts[0].value not in self.LDT.keys():
                self._errors.append(NotFoundError(node.lineno))
                return None
            if self.LDT[node.parts[0].value].type in ('CUINT', 'CBOOL'):
                self._errors.append(ConstAssignment(node.lineno))
                return None
            elif self.LDT[node.parts[0].value].type == 'BOOL':
                res = self._int_nd(node.parts[1])
                if res in (0, 1):
                    self.LDT[node.parts[0].value].value = res
                else:
                    self._errors.append(BadBoolAssignment(node.lineno))
                    self.LDT[node.parts[0].value].value = 1
                    return None
                return self.LDT[node.parts[0].value].value
            elif self.LDT[node.parts[0].value].type == 'UINT':
                res = self._int_nd(node.parts[1])
                if res is not None:
                    self.LDT[node.parts[0].value].value = res
                else:
                    self._errors.append(NoneTypeError(node.lineno))
                    return None
                return self.LDT[node.parts[0].value].value
            elif self.LDT[node.parts[0].value].type == '1DARRINT':
                index = self._int_nd(node.parts[1])
                val = self._int_nd(node.parts[2])
                if index is not None and val is not None:
                    try:
                        self.LDT[node.parts[0].value].value[index] = val
                        return self.LDT[node.parts[0].value].value[index]
                    except IndexError as ie:
                        self._errors.append(ie)
                        return None
            elif self.LDT[node.parts[0].value].type == '1DARRBOOL':
                res = self._int_nd(node.parts[2])
                index = self._int_nd(node.parts[1])
                try:
                    if (res in (0, 1)) and index is not None:
                        self.LDT[node.parts[0].value].value[index] = res
                    else:
                        self._errors.append(BadBoolAssignment(node.lineno))
                        self.LDT[node.parts[0].value].value[index] = 1
                        return None
                    return self.LDT[node.parts[0].value].value[index]
                except (IndexError, TypeError) as ie:
                    self._errors.append(ie)
                    return None
            elif self.LDT[node.parts[0].value].type == '2DARRINT':
                index1 = self._int_nd(node.parts[1])
                index2 = self._int_nd(node.parts[2])
                val = self._int_nd(node.parts[3])
                try:
                    if val is not None:
                        self.LDT[node.parts[0].value].value[index1][index2] = val
                    else:
                        self._errors.append(NoneTypeError(node.lineno))
                        return None
                except IndexError as ie:
                    self._errors.append(ie)
                    return None
            elif self.LDT[node.parts[0].value].type == '2DARRBOOL':
                index1 = self._int_nd(node.parts[1])
                index2 = self._int_nd(node.parts[2])
                val = self._int_nd(node.parts[3])
                if val in (0, 1) and index1 is not None and index2 is not None:
                    self.LDT[node.parts[0].value].value[index1][index2] = val
                else:
                    self._errors.append(BadBoolAssignment(node.lineno))
                    try:
                        self.LDT[node.parts[0].value].value[index1][index2] = 1
                    except (IndexError, TypeError) as e:  # TypeError or IndexError
                        self._errors.append(e)
                        return None
                    return None

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
                self._errors.append(RedeclarationError(node.lineno))
                return None
            self.LDT[node.parts[0].value] = Descriptor(node.value, [], None)
            if node.value == '1DARRBOOL':
                for i in node.parts[1:]:
                    res = self._int_nd(i)
                    if res in (0, 1):
                        self.LDT[node.parts[0].value].value.append(res)
                    else:
                        self._errors.append(BadBoolAssignment(node.lineno))
                        self.LDT[node.parts[0].value].value.append(1)
            else:
                self.LDT[node.parts[0].value].value = [self._int_nd(i) for i in node.parts[1:] if self._int_nd(i) is not None]
            self.LDT[node.parts[0].value].value.reverse()

        elif node.type == 'index_1d':
            if node.parts[0].value not in self.LDT.keys():
                self._errors.append(NotFoundError(node.lineno))
                return None
            if self.LDT[node.parts[0].value].type not in ('1DARRINT', '1DARRBOOL'):
                self._errors.append(InvalidIndexingObject(node.lineno))
            index = self._int_nd(node.parts[1])
            if index is not None:
                return self.LDT[node.parts[0].value].value[index]
            else:
                self._errors.append(NoneTypeError(node.lineno))
                return None

        elif node.type == 'index_2d':
            if node.parts[0].value not in self.LDT.keys():
                self._errors.append(NotFoundError(node.lineno))
                return None
            index1 = self._int_nd(node.parts[1])
            index2 = self._int_nd(node.parts[2])
            if index1 is not None and index2 is not None:
                try:
                    res = self.LDT[node.parts[0].value].value[index1][index2]
                    return res
                except IndexError as ie:
                    self._errors.append(ie)
                    return None
            else:
                self._errors.append(NoneTypeError(node.lineno))
                return None

        elif node.type == 'size_1d':
            if node.parts[0].value not in self.LDT.keys():
                self._errors.append(NotFoundError(node.lineno))
                return None
            return len(self.LDT[node.parts[0].value].value)

        elif node.type == 'size_2d':
            if node.parts[0].value not in self.LDT.keys():
                self._errors.append(NotFoundError(node.lineno))
                return None
            index = self._int_nd(node.parts[1])
            if index is not None:
                try:
                    return len(self.LDT[node.parts[0].value].value[index])
                except IndexError as ie:
                    self._errors.append(ie)
                    return None
            else:
                self._errors.append(NoneTypeError(node.lineno))
                return None

        elif node.type == 'extend1':
            if node.parts[0].value not in self.LDT.keys():
                self._errors.append(NotFoundError(node.lineno))
                return None
            if self.LDT[node.parts[0].value].type in ('1DARRINT', '1DARRBOOL'):
                if self._int_nd(node.parts[1]) < 0 or self._int_nd(node.parts[1]) is None:
                    self._errors.append(BadExtension(node.lineno))
                    return None
                extension = [0 for _ in range(self._int_nd(node.parts[1]))]
                self.LDT[node.parts[0].value].value.extend(extension)
            elif self.LDT[node.parts[0].value].type in ('2DARRBOOL', '2DARRINT'):
                ext_ln = self._int_nd(node.parts[1])
                int_ln = len(self.LDT[node.parts[0].value].value[-1])
                if ext_ln < 0 or ext_ln is None:
                    self._errors.append(BadExtension(node.lineno))
                    return None
                extension = [[0 for _ in range(int_ln)] for _ in range(ext_ln)]
                self.LDT[node.parts[0].value].value.extend(extension)
            else:
                self._errors.append(InvalidArrayOperator(node.lineno))
                return None

        elif node.type == 'create_2darr':
            if node.parts[0].value in self.LDT.keys():
                self._errors.append(RedeclarationError(node.lineno))
                return None
            self.LDT[node.parts[0].value] = Descriptor(node.value, [[]], None)
            if node.value == '2DARRBOOL':
                for i in range(1, len(node.parts)):
                    for j in range(len(node.parts[i].value)):
                        if self._int_nd(node.parts[i].value[j]) not in (0, 1):
                            self._errors.append(BadBoolAssignment(node.lineno))
                            node.parts[i].value[j] = STNode('number', 1, -1)
            try:
                self.LDT[node.parts[0].value].value = list(
                    map(lambda x: list(map(self._int_nd, x.value)), node.parts[1:]))
            except TypeError as te:
                self._errors.append(te)
                return None
            except IndexError as ie:
                self._errors.append(ie)
                return None
            for i in self.LDT[node.parts[0].value].value:
                i.reverse()
            self.LDT[node.parts[0].value].value.reverse()

        elif node.type == 'extend2':
            if node.parts[0].value not in self.LDT.keys():
                self._errors.append(NotFoundError(node.lineno))
                return None
            if self.LDT[node.parts[0].value].type in ('2DARRBOOL', '2DARRINT'):
                index = self._int_nd(node.parts[1])
                ext_ln = self._int_nd(node.parts[2])
                if ext_ln < 0 or ext_ln is None:
                    self._errors.append(BadExtension(node.lineno))
                    return None
                extension = [0 for _ in range(ext_ln)]
                self.LDT[node.parts[0].value].value[index].extend(extension)
            else:
                self._errors.append(InvalidArrayOperator(node.lineno))
                return None

        elif node.type == 'declare':
            if node.parts[0].value in self.LDT.keys():
                self._errors.append(RedeclarationError(node.lineno))
                return None
            node.parts[-1].value.reverse()
            self.LDT[node.parts[0].value] = Descriptor(node.value,
                                                       None,
                                                       node)
            self._functions[node.parts[0].value] = self.LDT[node.parts[0].value] = self.LDT[node.parts[0].value]

        elif node.type == 'call':
            if node.value.value not in self.LDT.keys():
                self._errors.append(NotFoundError(node.lineno))
                return None
            if len(self.nmsp_stack) > 100:
                self._errors.append(RecursionStackOverflow(node.lineno))
                return None
            fptr = self.LDT[node.value.value].link  # link to the function declaration
            sets = node.parts[0].value[:]
            pars = node.parts[1].value[:]
            sets.reverse()  # reverse the args' lists
            pars.reverse()
            args = self.parse_args(pars)
            self.nmsp_stack.append(self.LDT)
            self.LDT = {}
            for f in self._functions.keys():
                self.LDT[f] = self._functions[f]
            self.create_vars(fptr.parts[-1].value)  # create parameters and return values inside the function
            self.create_vars(fptr.parts[-2].value)
            self.asgn_args(fptr.parts[-1].value, args)
            self._int_nd(fptr.parts[1])  # execute body
            ret_values = self.collect_rets(fptr.parts[-2].value)
            self.LDT = self.nmsp_stack.pop()
            self.asgn_rets(node.parts[0].value, ret_values)  # assign ret-values

        elif node.type == 'command':
            if self.field is None or self.robot is None:
                self._errors.append(NoFieldError(node.lineno))
                return
            if node.value == 'forw':
                self.robot.cmd = None
                if self.field[self.robot.x - 1][self.robot.y].type == 'wall':
                    return 0
                self.robot.x -= 1
                if self.field[self.robot.x][self.robot.y].type == 'exit':
                    raise ExitFound(self.robot.x - 1, self.robot.y - 1)
                return 1

            elif node.value == 'back':
                self.robot.cmd = None
                if self.field[self.robot.x + 1][self.robot.y].type == 'wall':
                    return 0
                self.robot.x += 1
                if self.field[self.robot.x][self.robot.y].type == 'exit':
                    raise ExitFound(self.robot.x - 1, self.robot.y - 1)
                return 1

            elif node.value == 'right':
                self.robot.cmd = None
                if self.field[self.robot.x][self.robot.y + 1].type == 'wall':
                    return 0
                self.robot.y += 1
                if self.field[self.robot.x][self.robot.y].type == 'exit':
                    raise ExitFound(self.robot.x - 1, self.robot.y - 1)
                return 1

            elif node.value == 'left':
                self.robot.cmd = None
                if self.field[self.robot.x][self.robot.y - 1].type == 'wall':
                    return 0
                self.robot.y -= 1
                if self.field[self.robot.x][self.robot.y].type == 'exit':
                    raise ExitFound(self.robot.x - 1, self.robot.y - 1)
                return 1

            elif node.value == 'pushf':
                if self.field[self.robot.x - 1][self.robot.y].type != 'wall':
                    self.robot.cmd = None
                    return -1
                if self.robot.x - 2 < 0:
                    self.robot.cmd = None
                    return 0
                if self.field[self.robot.x - 2][self.robot.y].type in ('wall', 'exit'):
                    self.robot.cmd = None
                    return 0
                self.field[self.robot.x - 2][self.robot.y].type = 'wall'
                self.field[self.robot.x - 1][self.robot.y].type = 'plain'
                self.robot.cmd = 'pushf'
                return 1

            elif node.value == 'pushb':
                if self.field[self.robot.x + 1][self.robot.y].type != 'wall':
                    self.robot.cmd = None
                    return -1
                if self.robot.x + 2 > len(self.field):
                    self.robot.cmd = None
                    return 0
                if self.field[self.robot.x + 2][self.robot.y].type in ('wall', 'exit'):
                    self.robot.cmd = None
                    return 0
                self.field[self.robot.x + 2][self.robot.y].type = 'wall'
                self.field[self.robot.x + 1][self.robot.y].type = 'plain'
                self.robot.cmd = 'pushb'
                return 1

            elif node.value == 'pushl':
                if self.field[self.robot.x][self.robot.y - 1].type != 'wall':
                    self.robot.cmd = None
                    return -1
                if self.robot.y - 2 < 0:
                    self.robot.cmd = None
                    return 0
                if self.field[self.robot.x][self.robot.y - 2].type in ('wall', 'exit'):
                    self.robot.cmd = None
                    return 0
                self.field[self.robot.x][self.robot.y - 2].type = 'wall'
                self.field[self.robot.x][self.robot.y - 1].type = 'plain'
                self.robot.cmd = 'pushl'
                return 1

            elif node.value == 'pushr':
                if self.field[self.robot.x][self.robot.y + 1].type != 'wall':
                    self.robot.cmd = None
                    return -1
                if self.robot.y + 2 > len(self.field):
                    self.robot.cmd = None
                    return 0
                elif self.field[self.robot.x][self.robot.y + 2].type in ('wall', 'exit'):
                    self.robot.cmd = None
                    return 0
                self.field[self.robot.x][self.robot.y + 2].type = 'wall'
                self.field[self.robot.x][self.robot.y + 1].type = 'plain'
                self.robot.cmd = 'pushr'
                return 1

            elif node.value == 'undo':
                if self.robot.cmd == 'pushf':
                    self.field[self.robot.x - 2][self.robot.y].type = 'plain'
                    self.field[self.robot.x - 1][self.robot.y].type = 'wall'
                elif self.robot.cmd == 'pushb':
                    self.field[self.robot.x - 2][self.robot.y].type = 'plain'
                    self.field[self.robot.x - 1][self.robot.y].type = 'wall'
                elif self.robot.cmd == 'pushr':
                    self.field[self.robot.x][self.robot.y + 2].type = 'plain'
                    self.field[self.robot.x][self.robot.y + 1].type = 'wall'
                elif self.robot.cmd == 'pushl':
                    self.field[self.robot.x][self.robot.y - 2].type = 'plain'
                    self.field[self.robot.x][self.robot.y - 1].type = 'wall'
                else:
                    return 0
                return 1

            elif node.value == 'getf':
                self.robot.cmd = None
                dist = sys.maxsize * 2
                for i in range(0, self.robot.x + 1):
                    for j in range(0, len(self.field[i])):
                        if self.field[i][j].type == 'exit':
                            dist = min(dist, (abs(i - self.robot.x) + abs(j - self.robot.y)))
                return dist

            elif node.value == 'getb':
                self.robot.cmd = None
                dist = sys.maxsize * 2
                for i in range(self.robot.x, len(self.field)):
                    for j in range(0, len(self.field[i])):
                        if self.field[i][j].type == 'exit':
                            dist = min(dist, (abs(i - self.robot.x) + abs(j - self.robot.y)))
                return dist

            elif node.value == 'getl':
                self.robot.cmd = None
                dist = sys.maxsize * 2
                for i in range(0, len(self.field)):
                    for j in range(0, self.robot.y + 1):
                        if self.field[i][j].type == 'exit':
                            dist = min(dist, (abs(i - self.robot.x) + abs(j - self.robot.y)))
                return dist

            elif node.value == 'getr':
                self.robot.cmd = None
                dist = sys.maxsize * 2
                for i in range(0, len(self.field)):
                    for j in range(self.robot.y, len(self.field[i])):
                        if self.field[i][j].type == 'exit':
                            dist = min(dist, (abs(i - self.robot.x) + abs(j - self.robot.y)))
                return dist


if __name__ == '__main__':
    interpreter = Interpreter()
    # while True:
    #     interpreter.interpret(input())

    with open('testdata/fib', 'r') as f:
        data = f.read()
    interpreter.interpret(data)
