import time

cars = {}
visited = []
visited_depths = []
stack = []
stack_depths = []


def init(file_path):
    global cars
    crossroad = [['0'] * 6 for _i in range(6)]
    file = open(file_path, "r")
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


def move_combo(crossroad, car_name, curr_depth, depth, direction):
    global cars
    global visited
    steps = max_step(crossroad, car_name, direction)
    temp = [list(x) for x in crossroad]
    curr_depth += 1
    if curr_depth > depth:
        return
    for step in range(1, steps + 1):
        temp = [list(x) for x in temp]
        operator(temp, car_name, direction)

        if temp not in visited:
            stack.append(temp)
            stack_depths.append(curr_depth)


def dfs(initial_crossroad, depth):
    global cars
    global visited
    global visited_depths
    global stack
    global stack_depths
    curr_depth = 0
    stack = [initial_crossroad]
    stack_depths = [curr_depth]
    visited = [initial_crossroad]
    visited_depths = [curr_depth]
    while True:
        if len(stack) == 0:
            print("{} depth. Stack empty. Mission failed going deeper.".format(depth))
            return 0
        crossroad = stack.pop()
        curr_depth = stack_depths.pop()
        if visited_depths[-1] < curr_depth:
            visited.append(crossroad)
            visited_depths.append(curr_depth)
        elif visited_depths[-1] == curr_depth:
            visited[-1] = crossroad
        else:
            while visited_depths[-1] > curr_depth:
                visited.pop()
                visited_depths.pop()
            visited[-1] = crossroad
            visited_depths[-1] = curr_depth

        for i in range(len(crossroad)):     # prvé (červené) auto sa nachádza na konci križovatky
            if crossroad[i][5] == 'A':
                print("{} depth. najdene riesenie".format(depth))
                return 1

        if curr_depth == depth:
            continue
        for car_name in cars.keys():
            if cars[car_name]["direction"] == "h":
                move_combo(crossroad, car_name, curr_depth, depth, "right")
                move_combo(crossroad, car_name, curr_depth, depth, "left")
            elif cars[car_name]["direction"] == "v":
                move_combo(crossroad, car_name, curr_depth, depth, "down")
                move_combo(crossroad, car_name, curr_depth, depth, "up")


def iterative_dfs():
    global cars
    for depth in range(8):
        crossroad = init("maps/cars_1.txt")
        end = dfs(crossroad, depth)
        if end == 1:
            return 1
    print("riesenie sa nenaslo")
    return 0


def start():
    print("""-------------------------------------------------------------
    Dobrý večer, dobrý večer. Hráte hru Multikrižovatkár.
   -------------------------------------------------------
    """)
    start_time = time.time()
    done = iterative_dfs()
    end_time = time.time()
    if done == 1:
        counter = 0
        for cross in visited:
            print("{}. move".format(counter))
            print_crossroad(cross)
            counter += 1
    print("Compilation time: {} seconds".format(round(end_time - start_time, 2)))


start()
