import interpreter
import maze


def control():
    print('Input the filename of the map file:')
    filename = input()
    try:
        fld, robot = maze.read_map(filename)
    except FileNotFoundError as fn:
        print(fn)
        fld, robot = None, None
    print('Input the filename for reading the language and robot instructions:')
    filename = input()
    try:
        with open(filename) as w:
            data = w.read()
        controller = interpreter.Interpreter(fld, robot)
    except FileNotFoundError as fn:
        print(fn)
        return
    try:
        controller.interpret(data)
    except interpreter.ExitFound as ex:
        print(ex)
        return
    print('Robot could not find the exit!')


if __name__ == '__main__':
    control()
