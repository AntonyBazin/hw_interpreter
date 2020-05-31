import interpreter
import maze

if __name__ == '__main__':
    # print('Input map file name:')
    # name = input()
    try:
        fld, robot = maze.read_map('testdata/map')
    except FileNotFoundError as fn:
        print(fn)
        fld, robot = None, None
    with open('testdata/way') as w:
        data = w.read()
    controller = interpreter.Interpreter(fld, robot)
    try:
        controller.interpret(data)
    except interpreter.ExitFound as ex:
        print(ex)
