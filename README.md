# Interpreter

A simple non-optimizing interpreter written in Python 3.

## Installation

Use the package manager [pip](https://pypi.org/project/pip/) to install PLY:

```bash
pip install ply
```

## Usage

To run the standard example calculating the Nth Fibonacci's sequence number, type in the console:

```bash
python3 interpreter.py 
```
Then, type the ```fib.txt``` filename.

### Note 
You can also give the interpreter the ```gnome.txt``` file for running a simple gnome sort implementation.

## Robot
To run the standard robot pathfinding algorithm, type:

```bash
python3 runner.py
```
The script will first ask you for the name of the file containing the map, then the name of the file with instructions. If the script won't be able to read the map, it will notify you.
There is a pre-written ```map.txt``` file containing the map, ```way.txt``` containing the pathfinding algorithm, and ```way2.txt``` which can be used to demonstrate the robot's abilities.


## License
[MIT](https://choosealicense.com/licenses/mit/)
