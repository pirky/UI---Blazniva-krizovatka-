from copy import *


class Car:
    def __init__(self, size, line, column, direction):
        self.size = size
        self.line = line
        self.column = column
        self.direction = direction

    def __eq__(self, other):
        if not isinstance(other, Car):
            return NotImplemented
        else:
            return self.size == other.size and self.line == other.line and \
                   self.column == other.column and self.direction == other.direction


class State:
    def __init__(self, crossroad, cars, depth):
        self.crossroad = crossroad
        self.cars = cars
        self.depth = depth

    def __eq__(self, other):
        if not isinstance(other, State):
            return NotImplemented
        else:
            return self.crossroad == other.crossroad and self.cars == other.cars


class Node:
    def __init__(self, state, prevnode, visited):
        self.state = state
        self.prevNode = prevnode
        self.visited = visited

    def set_visit(self, visited):
        self.visited = visited


def init():
    crossroad = [['0'] * 6 for _i in range(6)]
    cars = []
    file = open("cars.txt", "r")
    for line in file:
        arr = line.split()
        car = Car(int(arr[0]), int(arr[1]) - 1, int(arr[2]) - 1, arr[3])
        for i in range(car.size):
            if car.direction == 'v':
                crossroad[car.line + i][car.column] = '1'
            else:
                crossroad[car.line][car.column + i] = '1'
        cars.append(car)
    file.close()
    return State(crossroad, cars, 0)


def print_crossroad(crossroad):
    for line in crossroad:
        print(line)
    print("\n")


def right(state, car_position):
    car = state.cars[car_position]
    crossroad = state.crossroad
    for i in range(car.size):
        crossroad[car.line][car.column + i] = '0'
    car.column += 1
    for i in range(car.size):
        crossroad[car.line][car.column + i] = '1'


def left(state, car_position):
    car = state.cars[car_position]
    crossroad = state.crossroad
    for i in range(car.size):
        crossroad[car.line][car.column + i] = '0'
    car.column -= 1
    for i in range(car.size):
        crossroad[car.line][car.column + i] = '1'


def up(state, car_position):
    car = state.cars[car_position]
    crossroad = state.crossroad
    for i in range(car.size):
        crossroad[car.line + i][car.column] = '0'
    car.line -= 1
    for i in range(car.size):
        crossroad[car.line + i][car.column] = '1'


def down(state, car_position):
    car = state.cars[car_position]
    crossroad = state.crossroad
    for i in range(car.size):
        crossroad[car.line + i][car.column] = '0'
    car.line += 1
    for i in range(car.size):
        crossroad[car.line + i][car.column] = '1'


def max_step(car, crossroad, direction):
    steps = 0
    if direction == "right":
        while car.column + car.size + steps < 6:
            field = crossroad[car.line][car.column + car.size + steps]
            if field == '1':
                break
            steps += 1

    elif direction == "left":
        while car.column - steps - 1 > -1:
            field = crossroad[car.line][car.column - steps - 1]
            if field == '1':
                break
            steps += 1

    elif direction == "down":
        while car.line + car.size + steps < 6:
            field = crossroad[car.line + car.size + steps][car.column]
            if field == '1':
                break
            steps += 1

    elif direction == "up":
        while car.line - steps - 1 > -1:
            field = crossroad[car.line - steps - 1][car.column]
            if field == '1':
                break
            steps += 1

    return steps


def move_combo(state, iteror, visited, stack, depth, direction):
    steps = max_step(state.cars[iteror], state.crossroad, direction)
    temp = deepcopy(state)
    temp.depth += 1
    if temp.depth > depth:
        return 0
    for step in range(1, steps + 1):
        temp = deepcopy(temp)
        if direction == "right":
            right(temp, iteror)
        elif direction == "left":
            left(temp, iteror)
        elif direction == "down":
            down(temp, iteror)
        elif direction == "up":
            up(temp, iteror)

        if temp in visited:
            index = visited.index(temp)
            if temp == visited[index] and temp.depth < visited[index].depth:
                stack.append(temp)
                visited.remove(visited[index])
                visited.append(temp)
                break
        else:
            stack.append(temp)

        if temp.cars[0].column + temp.cars[0].size - 1 == 5:    # prvé (červené) auto sa nachádza na konci križovatky
            return 1
    return 0


def dfs(first_state, depth):
    stack = [first_state]
    visited = []
    while True:
        if len(stack) == 0:
            print("{} depth Stack empty. Mission failed going deeper.".format(depth))
            break
        state = stack.pop()
        visited.append(state)
        if state.depth > depth:
            continue
        for i in range(len(state.cars)):
            if state.cars[i].direction == "h":
                end = move_combo(state, i, visited, stack, depth, "right")
                if end == 1:
                    print_crossroad(stack.pop().crossroad)
                    return 1
                move_combo(state, i, visited, stack, depth, "left")
            elif state.cars[i].direction == "v":
                move_combo(state, i, visited, stack, depth, "down")
                move_combo(state, i, visited, stack, depth, "up")

    return 0


def iterative_dfs():
    for depth in range(8, 9):
        state = init()
        end = dfs(state, depth)
        if end == 1:
            break


def start():
    print("""-------------------------------------------------------------
    Dobrý večer, dobrý večer. Hráte hru Multikrižovatkár.
   -------------------------------------------------------
    """)
    iterative_dfs()


start()
