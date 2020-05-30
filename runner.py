import interpreter
import maze

if __name__ == '__main__':
    # print('Input map file name:')
    # name = input()
    try:
        fld = maze.read_map('testdata/map')
    except FileNotFoundError as fn:
        print(fn)
        fld = None
    interpreter = interpreter.Interpreter(fld)

