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


def init():
    crossroad = [['0'] * 6 for _i in range(6)]
    cars = {}
    file = open("cars.txt", "r")
    char_num = 65
    for line in file:
        arr = line.split()
        car_name = chr(char_num)
        char_num += 1
        cars[car_name] = dict([("size", int(arr[0])), ("direction", arr[3])])
        for i in range(cars[car_name]["size"]):
            if cars[car_name]["direction"] == 'v':
                crossroad[int(arr[1]) + i][int(arr[2])] = car_name
            else:
                crossroad[int(arr[1])][int(arr[2]) + i] = car_name
    file.close()
    return cars, crossroad


def print_crossroad(crossroad):
    for line in crossroad:
        print(line)
    print("\n")


def operator(crossroad, cars, car_name, direction):
    first = car_line = car_column = i = 0
    for line in crossroad:
        j = 0
        for char in line:
            if char == car_name:
                crossroad[i][j] = "0"
                if first == 0:
                    first = 1
                    if direction == "right":
                        car_line = i
                        car_column = j + 1
                    elif direction == "left":
                        car_line = i
                        car_column = j - 1
                    elif direction == "up":
                        car_line = i - 1
                        car_column = j
                    elif direction == "down":
                        car_line = i + 1
                        car_column = j
            j += 1
        i += 1
    for i in range(cars[car_name]["size"]):
        if direction == "right" or direction == "left":
            crossroad[car_line][car_column + i] = car_name
        else:
            crossroad[car_line + i][car_column] = car_name


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
        # if direction == "right":
        #     right(temp, iteror)
        # elif direction == "left":
        #     left(temp, iteror)
        # elif direction == "down":
        #     down(temp, iteror)
        # elif direction == "up":
        #     up(temp, iteror)

        if temp in visited:
            index = visited.index(temp)
            if temp == visited[index] and temp.depth < visited[index].depth:
                stack.append(temp)
                visited.remove(visited[index])
                visited.append(temp)
                break
        else:
            stack.append(temp)

        if temp.cars[0].column + temp.cars[0].size - 1 == 5:  # prvé (červené) auto sa nachádza na konci križovatky
            return 1
    return 0


def dfs(cars, initial_crossroad, depth):
    stack = [initial_crossroad]
    number_of_cars = len(cars)
    visited = []
    print_crossroad(initial_crossroad)
    operator(initial_crossroad, cars, "F", "left")
    print_crossroad(initial_crossroad)
    # while True:
    #     if len(stack) == 0:
    #         print("{} depth Stack empty. Mission failed going deeper.".format(depth))
    #         break
    #     crossroad = stack.pop()
    #     visited.append(crossroad)
    #
    #     for i in range(number_of_cars):
    #         if state.cars[i].direction == "h":
    #             end = move_combo(state, i, visited, stack, depth, "right")
    #             if end == 1:
    #                 print_crossroad(stack.pop().crossroad)
    #                 return 1
    #             move_combo(state, i, visited, stack, depth, "left")
    #         elif state.cars[i].direction == "v":
    #             move_combo(state, i, visited, stack, depth, "down")
    #             move_combo(state, i, visited, stack, depth, "up")

    return 0


def iterative_dfs():
    for depth in range(1):
        cars, crossroad = init()
        end = dfs(cars, crossroad, depth)
        if end == 1:
            return
    print("riesenie sa nenaslo")


def start():
    print("""-------------------------------------------------------------
    Dobrý večer, dobrý večer. Hráte hru Multikrižovatkár.
   -------------------------------------------------------
    """)
    iterative_dfs()


def halabala():
    print()


start()
