import time
from colorama import Fore


cars = {}
visited = []
visited_depths = []
stack = []
stack_depths = []
path = []
path_depths = []


def init_bez_objektov():
    global cars
    crossroad = [['0'] * 6 for _i in range(6)]
    file = open("maps/cars_5.txt", "r")
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


def print_operators(crossroad_1, crossroad_2):
    cars_1 = {}
    cars_2 = {}
    car_line = 0
    for line in crossroad_1:
        car_column = 0
        for char in line:
            if char != "0":
                if char not in cars_1:
                    cars_1[char] = {"line": car_line, "column": car_column, "size": 1}
                else:
                    cars_1[char]["size"] += 1
            car_column += 1
        car_line += 1

    car_line = 0
    for line in crossroad_2:
        car_column = 0
        for char in line:
            if char != "0":
                if char not in cars_2:
                    cars_2[char] = {"line": car_line, "column": car_column, "size": 1}
                else:
                    cars_2[char]["size"] += 1
            car_column += 1
        car_line += 1

    car_name = 65
    for i in range(len(cars_1)):
        if cars_1[chr(car_name + i)] != cars_2[chr(car_name + i)]:
            if cars_1[chr(car_name + i)]["line"] == cars_2[chr(car_name + i)]["line"]:
                move = cars_1[chr(car_name + i)]["column"] - cars_2[chr(car_name + i)]["column"]
                if move < 0:
                    print("\n\"{}\" -> {} right.".format(chr(car_name + i), abs(move)))
                else:
                    print("\n\"{}\" -> {} left.".format(chr(car_name + i), abs(move)))
            else:
                move = cars_1[chr(car_name + i)]["line"] - cars_2[chr(car_name + i)]["line"]
                if move < 0:
                    print("\n\"{}\" -> {} down.".format(chr(car_name + i), abs(move)))
                else:
                    print("\n\"{}\" -> {} up.".format(chr(car_name + i), abs(move)))


def print_crossroad(crossroad):
    print()
    for line in crossroad:
        for char in line:
            if char == "0":
                print(char, end=' ')
            elif ord(char) % 15 == 0:
                print(Fore.LIGHTYELLOW_EX + char, end=' ')
            elif ord(char) % 15 == 1:
                print(Fore.LIGHTBLACK_EX + char, end=' ')
            elif ord(char) % 15 == 2:
                print(Fore.LIGHTWHITE_EX + char, end=' ')
            elif ord(char) % 15 == 4:
                print(Fore.LIGHTRED_EX + char, end=' ')
            elif ord(char) % 15 == 5:
                print(Fore.RED + char, end=' ')
            elif ord(char) % 15 == 6:
                print(Fore.CYAN + char, end=' ')
            elif ord(char) % 15 == 7:
                print(Fore.YELLOW + char, end=' ')
            elif ord(char) % 15 == 8:
                print(Fore.GREEN + char, end=' ')
            elif ord(char) % 15 == 9:
                print(Fore.BLUE + char, end=' ')
            elif ord(char) % 15 == 10:
                print(Fore.MAGENTA + char, end=' ')
            elif ord(char) % 15 == 11:
                print(Fore.LIGHTBLUE_EX + char, end=' ')
            elif ord(char) % 15 == 12:
                print(Fore.LIGHTCYAN_EX + char, end=' ')
            elif ord(char) % 15 == 13:
                print(Fore.LIGHTGREEN_EX + char, end=' ')
            elif ord(char) % 15 == 14:
                print(Fore.LIGHTMAGENTA_EX + char, end=' ')
            print(Fore.RESET, end='')

        print()


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


def move_combo_bez_objektov(crossroad, car_name, curr_depth, depth, direction):
    global cars
    global visited
    global visited_depths
    global stack
    global stack_depths

    steps = max_step_bez_objektov(crossroad, car_name, direction)
    curr_depth += 1
    if curr_depth > depth:
        return
    for step in range(1, steps + 1):
        crossroad = [list(x) for x in crossroad]
        operator_bez_objektov(crossroad, car_name, direction)

        if crossroad in visited:
            index = visited.index(crossroad)
            if curr_depth < visited_depths[index]:
                stack.append(crossroad)
                stack_depths.append(curr_depth)
                visited[index] = crossroad
                visited_depths[index] = curr_depth
        else:
            stack.append(crossroad)
            stack_depths.append(curr_depth)


def update_path(curr_depth, crossroad):
    global path
    global path_depths
    if path_depths[-1] < curr_depth:
        path.append(crossroad)
        path_depths.append(curr_depth)
    elif path_depths[-1] == curr_depth:
        path[-1] = crossroad
    else:
        while path_depths[-1] > curr_depth:
            path.pop()
            path_depths.pop()
        path[-1] = crossroad
        path_depths[-1] = curr_depth


def dfs_bez_objektov(initial_crossroad, depth):
    global cars
    global visited
    global visited_depths
    global stack
    global stack_depths
    global path
    global path_depths
    curr_depth = 0
    stack = [initial_crossroad]
    stack_depths = [curr_depth]
    path = [initial_crossroad]
    path_depths = [curr_depth]
    visited = []
    visited_depths = []
    while True:
        if len(stack) == 0:
            print("{} depth. Stack empty. Mission failed going deeper.".format(depth))
            return 0

        crossroad = stack.pop()
        curr_depth = stack_depths.pop()
        visited.append(crossroad)
        visited_depths.append(curr_depth)
        update_path(curr_depth, crossroad)

        for i in range(len(crossroad)):     # prvé (červené) auto sa nachádza na konci križovatky
            if crossroad[i][5] == 'A':
                print("{} depth. Finito.".format(depth))
                return 1

        if curr_depth > depth:
            continue

        for car_name in cars.keys():
            if cars[car_name]["direction"] == "h":
                move_combo_bez_objektov(crossroad, car_name, curr_depth, depth, "right")
                move_combo_bez_objektov(crossroad, car_name, curr_depth, depth, "left")
            elif cars[car_name]["direction"] == "v":
                move_combo_bez_objektov(crossroad, car_name, curr_depth, depth, "down")
                move_combo_bez_objektov(crossroad, car_name, curr_depth, depth, "up")


def iterative_dfs_bez_objektov():
    global cars
    for depth in range(18):
        crossroad = init_bez_objektov()
        end = dfs_bez_objektov(crossroad, depth)
        if end == 1:
            return 1
    return 0


def start_bez_objektov():
    print("""-------------------------------------------------------------
    Dobrý večer, dobrý večer. Hráte hru Multikrižovatkár.
   -------------------------------------------------------
    """)
    start_time = time.time()
    done = iterative_dfs_bez_objektov()
    end_time = time.time()
    if done == 1:
        counter = 0
        for crossroad in path:
            if 0 < counter < len(path):
                print("\n{}. move".format(counter))
                print_operators(path[counter - 1], path[counter])
            else:
                print("\nStarting crossroad:")
            print_crossroad(crossroad)
            counter += 1
    else:
        print("riesenie sa nenaslo")
    print("\nCompilation time: {} seconds".format(round(end_time - start_time, 2)))


start_bez_objektov()
