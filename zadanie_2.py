

class Car:
    def __init__(self, size, line, column, direction, red):
        self.size = size
        self.line = line
        self.column = column
        self.direction = direction
        self.red = red


class State:
    def __init__(self, crossroad, cars):
        self.crossroad = crossroad
        self.cars = cars


class Node:
    def __init__(self, state, prevnode, visited):
        self.state = state
        self.prevNode = prevnode
        self.visited = visited

    def set_visit(self, visited):
        self.visited = visited


def init():
    crossroad = [['0'] * 6 for i in range(6)]
    cars = []
    file = open("cars.txt", "r")
    for line in file:
        arr = line.split()
        car = Car(int(arr[0]), int(arr[1]) - 1, int(arr[2]) - 1, arr[3], int(arr[4]))
        for i in range(car.size):
            if car.direction == 'v':
                crossroad[car.line + i][car.column] = '1'
            else:
                crossroad[car.line][car.column + i] = '1'
        cars.append(car)
    file.close()
    return State(crossroad, cars)


def right(state, car_position, step):
    car = state.cars[car_position]
    crossroad = state.crossroad
    move = car.column + car.size + step - 1
    if 0 <= move < 6:
        for i in range(car.size, car.size + step):
            if crossroad[car.line][car.column + i] == '1':
                return 0
        for i in range(car.size):
            crossroad[car.line][car.column + i] = '0'
        car.column += step
        for i in range(car.size):
            crossroad[car.line][car.column + i] = '1'
        return 1
    return 0


def left(state, car_position, step):
    car = state.cars[car_position]
    crossroad = state.crossroad
    move = car.column - step
    if 0 <= move < 6:
        for i in range(1, step + 1):
            if crossroad[car.line][car.column - i] == '1':
                return 0
        for i in range(car.size):
            crossroad[car.line][car.column + i] = '0'
        car.column -= step
        for i in range(car.size):
            crossroad[car.line][car.column + i] = '1'
        return 1
    return 0


def up(state, car_position, step):
    car = state.cars[car_position]
    crossroad = state.crossroad
    move = car.line - step
    if 0 <= move < 6:
        for i in range(1, step + 1):
            if crossroad[car.line - i][car.column] == '1':
                return 0
        for i in range(car.size):
            crossroad[car.line + i][car.column] = '0'
        car.line -= step
        for i in range(car.size):
            crossroad[car.line + i][car.column] = '1'
        return 1
    return 0


def down(state, car_position, step):
    car = state.cars[car_position]
    crossroad = state.crossroad
    move = car.line + car.size + step - 1
    if 0 <= move < 6:
        for i in range(car.size, car.size + step):
            if crossroad[car.line + i][car.column] == '1':
                return 0
        for i in range(car.size):
            crossroad[car.line + i][car.column] = '0'
        car.line += step
        for i in range(car.size):
            crossroad[car.line + i][car.column] = '1'
        return 1
    return 0


def print_crossroad(crossroad):
    for line in crossroad:
        print(line)
    print("\n")


def dfs():
    print()


def iterative_dfs():
    print()


def start():
    state = init()
    print_crossroad(state.crossroad)
    down(state, 4, 1)
    print_crossroad(state.crossroad)


start()
