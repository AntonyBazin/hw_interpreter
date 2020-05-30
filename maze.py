import os.path


class Map:
    """The entire map"""

    def __init__(self, sizex, sizey, cells):
        self.sizex = sizex
        self.sizey = sizey
        self.cells = cells


class Cell:
    """Describes a cell of the maze"""

    def __init__(self, tp):
        self.type = tp  # wall or plain or exit

    def __str__(self):
        return self.type


class Robot:
    """The robot"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'robot at ({0}, {1})'.format(self.x, self.y)


def read_map(name):
    if os.path.isfile(name):
        field = []
        path = []
        with open(name) as file:
            lines = file.readlines()
            x, y = (int(val) for val in lines[0].split())
            robot = Robot(x, y)
            for line in lines[1:]:
                for symbol in line:
                    if symbol == 'O':
                        path.append(Cell('plain'))
                    elif symbol == 'X':
                        path.append(Cell('exit'))
                    elif symbol == '%':
                        path.append(Cell('wall'))
                field.append(path)
                path = []
            return field, robot
    else:
        raise FileNotFoundError


if __name__ == '__main__':
    f, r = read_map('testdata/map')
    for i in f:
        for j in i:
            print(j)
        print()
    print(r)
