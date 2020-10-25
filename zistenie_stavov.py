import time


cars = {}
visited = []
visited_depths = []
stack = []
stack_depths = []
state_counter = 0


def init_bez_objektov():
    global cars
    crossroad = [['0'] * 6 for _i in range(6)]
    file = open("maps/cars_6.txt", "r")
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
    return crossroad


def operator_bez_objektov(crossroad, car_name, direction):
    global cars
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


def find_car_bez_objektov(crossroad, car_name):
    i = 0
    for line in crossroad:
        j = 0
        for char in line:
            if char == car_name:
                return i, j
            j += 1
        i += 1
    return None, None


def max_step_bez_objektov(crossroad, car_name, direction):
    global cars
    steps = 0
    car_line, car_column = find_car_bez_objektov(crossroad, car_name)
    car_size = cars[car_name]["size"]

    if direction == "right":
        while car_column + car_size + steps < 6:
            field = crossroad[car_line][car_column + car_size + steps]
            if field != '0':
                break
            steps += 1

    elif direction == "left":
        while car_column - steps - 1 > -1:
            field = crossroad[car_line][car_column - steps - 1]
            if field != '0':
                break
            steps += 1

    elif direction == "down":
        while car_line + car_size + steps < 6:
            field = crossroad[car_line + car_size + steps][car_column]
            if field != '0':
                break
            steps += 1

    elif direction == "up":
        while car_line - steps - 1 > -1:
            field = crossroad[car_line - steps - 1][car_column]
            if field != '0':
                break
            steps += 1

    return steps


def move_combo_bez_objektov(crossroad, car_name, direction):
    global cars
    global visited
    global stack
    global state_counter

    steps = max_step_bez_objektov(crossroad, car_name, direction)
    for step in range(1, steps + 1):
        crossroad = [list(x) for x in crossroad]
        operator_bez_objektov(crossroad, car_name, direction)

        if crossroad not in visited:
            visited.append(crossroad)
            stack.append(crossroad)


def dfs_bez_objektov(initial_crossroad):
    global cars
    global stack
    global visited
    global state_counter
    stack = [initial_crossroad]
    while True:
        if len(stack) == 0:
            return 0
        crossroad = stack.pop()
        state_counter += 1
        visited.append(crossroad)
        for car_name in cars.keys():
            if cars[car_name]["direction"] == "h":
                move_combo_bez_objektov(crossroad, car_name, "right")
                move_combo_bez_objektov(crossroad, car_name, "left")
            elif cars[car_name]["direction"] == "v":
                move_combo_bez_objektov(crossroad, car_name, "down")
                move_combo_bez_objektov(crossroad, car_name, "up")


def start_bez_objektov():
    crossroad = init_bez_objektov()
    dfs_bez_objektov(crossroad)
    print("\nState counter: {}".format(state_counter))


start_bez_objektov()
