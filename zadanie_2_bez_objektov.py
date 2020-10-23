import time

cars = {}


def init():
    global cars
    crossroad = [['0'] * 6 for _i in range(6)]
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
    return crossroad


def print_crossroad(crossroad):
    for line in crossroad:
        print(line)
    print("\n")


def operator(crossroad, car_name, direction):
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


# vrati poziciu auta
def find_car(crossroad, car_name):
    i = 0
    for line in crossroad:
        j = 0
        for char in line:
            if char == car_name:
                return i, j
            j += 1
        i += 1
    return None, None


def max_step(crossroad, car_name, direction):
    global cars
    steps = 0
    car_line, car_column = find_car(crossroad, car_name)
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


def move_combo(crossroad, car_name, visited, visited_depths, stack, stack_depths, curr_depth, depth, direction):
    global cars
    steps = max_step(crossroad, car_name, direction)
    temp = [list(x) for x in crossroad]
    curr_depth += 1
    if curr_depth > depth:
        return 0
    for step in range(1, steps + 1):
        temp = [list(x) for x in temp]
        operator(temp, car_name, direction)

        if temp in visited:
            index = visited.index(temp)
            if curr_depth < visited_depths[index]:
                stack.append(temp)
                stack_depths.append(curr_depth)
                visited[index] = temp
                visited_depths[index] = curr_depth
                break
        else:
            stack.append(temp)
            stack_depths.append(curr_depth)

        for i in range(len(temp)):     # prvé (červené) auto sa nachádza na konci križovatky
            if temp[i][5] == 'A':
                print("finito")
                return 1
    return 0


def dfs(initial_crossroad, depth):
    global cars
    curr_depth = 0
    stack = [initial_crossroad]
    stack_depths = [curr_depth]
    visited = []
    visited_depths = []
    while True:
        if len(stack) == 0:
            print("{} depth. Stack empty. Mission failed going deeper.".format(depth))
            break
        crossroad = stack.pop()
        curr_depth = stack_depths.pop()
        if curr_depth > depth:
            continue
        visited.append(crossroad)
        visited_depths.append(curr_depth)
        for car_name in cars.keys():
            if cars[car_name]["direction"] == "h":
                end = move_combo(crossroad, car_name, visited, visited_depths, stack, stack_depths, curr_depth,
                                 depth, "right")
                if end == 1:
                    print_crossroad(stack.pop())
                    return 1
                move_combo(crossroad, car_name, visited, visited_depths, stack, stack_depths, curr_depth,
                           depth, "left")
            elif cars[car_name]["direction"] == "v":
                move_combo(crossroad, car_name, visited, visited_depths, stack, stack_depths, curr_depth,
                           depth, "down")
                move_combo(crossroad, car_name, visited, visited_depths, stack, stack_depths, curr_depth,
                           depth, "up")

    return 0


def iterative_dfs():
    global cars
    for depth in range(9):
        crossroad = init()
        end = dfs(crossroad, depth)
        if end == 1:
            return
    print("riesenie sa nenaslo")


def start():
    start_time = time.time()
    print("""-------------------------------------------------------------
    Dobrý večer, dobrý večer. Hráte hru Multikrižovatkár.
   -------------------------------------------------------
    """)
    iterative_dfs()
    end_time = time.time()
    print("Compilation time: {} seconds".format(round(end_time - start_time, 2)))


start()
