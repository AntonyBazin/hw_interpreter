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


def read_map(name):
    if os.path.isfile(name):
        field = []
        path = []
        with open(name) as file:
            for line in file:
                for symbol in line:
                    if symbol == 'O':
                        path.append(Cell('plain'))
                    elif symbol == 'X':
                        path.append(Cell('exit'))
                    elif symbol == '%':
                        path.append(Cell('wall'))
                field.append(path)
                path = []
            return field
    else:
        raise FileNotFoundError


if __name__ == '__main__':
    f = read_map('testdata/map')
    for i in f:
        for j in i:
            print(j)
        print()
