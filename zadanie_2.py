import time
import datetime
from colorama import Fore


cars = {}
visited = []
visited_depths = []
stack = []
stack_depths = []


# Načítanie prvej križovatky a info o autách
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


# vypíše poradie operátorov
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


# Farebné vypísanie križovatky
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


# Posun auta daným smerom
def operator(crossroad, car_name, direction):
    global cars
    first = car_line = car_column = i = 0

    for line in crossroad:
        j = 0
        for char in line:
            if char == car_name:
                crossroad[i][j] = "0"  # vynuluje pozíciu auta
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

    for i in range(cars[car_name]["size"]):  # umiestni auto na jeho novú pozíciu
        if direction == "right" or direction == "left":
            crossroad[car_line][car_column + i] = car_name
        else:
            crossroad[car_line + i][car_column] = car_name


# vrati x(riadok),y(stĺpec) poziciu auta v križovatke
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


# vráti o koľko sa môže maximálne posunúť auto daným smerom
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


# pridá do stacku každé možné rozloženie aut, ak sa také už nenachádza v ceste od koreňa k danému uzlu
def move_combo(crossroad, car_name, curr_depth, direction):
    global cars
    global visited
    steps = max_step(crossroad, car_name, direction)
    for step in range(1, steps + 1):
        crossroad = [list(x) for x in crossroad]
        operator(crossroad, car_name, direction)

        if crossroad not in visited:
            stack.append(crossroad)
            stack_depths.append(curr_depth)


# upraví súčasnú cestu od koreňa k prehľadávanému vrcholu
def edit_visited(curr_depth, crossroad):
    global visited
    global visited_depths

    if visited_depths[-1] < curr_depth:         # ak som v nižšej hľbke pridám stav križovatky do cesty
        visited.append(crossroad)
        visited_depths.append(curr_depth)
    elif visited_depths[-1] == curr_depth:      # ak som na rovnakej hĺbke, tak vymením križovatky
        visited[-1] = crossroad
    else:
        while visited_depths[-1] > curr_depth:  # vymazávam križovatky pokiaľ nie som na rovnakej hĺbke,
            visited.pop()                       # z akej sa chystám pokračovať v prehľadávaní
            visited_depths.pop()                # nakoniec vymením križovatky
        visited[-1] = crossroad
        visited_depths[-1] = curr_depth


# algoritmus prehľadávania do hĺbky
def dfs(initial_crossroad, depth, debug):
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
        edit_visited(curr_depth, crossroad)

        if debug:
            print("\nCurrent depth -> {}\nMax depth -> {}".format(curr_depth, depth))
            if curr_depth > 0:
                print("\nParent crossroad")
                print_crossroad(visited[-2])
                print_operators(visited[-2], visited[-1])
            print_crossroad(visited[-1])
            input("\nPress \"Enter\" to continue\t")

        for i in range(len(crossroad)):  # prvé (červené) auto sa nachádza na konci križovatky
            if crossroad[i][5] == 'A':
                print("{} depth. This is the end.".format(depth))
                return 1

        if curr_depth == depth:
            continue

        curr_depth += 1
        for car_name in cars.keys():  # všetky možné posuny v danej križovatke sa pridajú do stacku
            if cars[car_name]["direction"] == "h":
                move_combo(crossroad, car_name, curr_depth, "right")
                move_combo(crossroad, car_name, curr_depth, "left")
            elif cars[car_name]["direction"] == "v":
                move_combo(crossroad, car_name, curr_depth, "down")
                move_combo(crossroad, car_name, curr_depth, "up")


# spustí DFS so zvyšujúcou sa hĺbkou
def iterative_dfs(debug, file_path, max_depth):
    global cars
    crossroad = init(file_path)
    for depth in range(max_depth + 1):
        end = dfs(crossroad, depth, debug)
        if end == 1:
            return 1
    return 0


# začiatok programu, zobrazí úvodné menu
def start():
    print("""-------------------------------------------------------------
    Dobrý večer, dobrý večer. Hráte hru Multikrižovatkár.
   -------------------------------------------------------
    """)
    file_path = input("Zadajte cestu k súboru:  ")       # maps/cars_1.txt
    max_depth = int(input("Zadajte hĺbku, do ktorej má program prehľadávať:  "))
    debug = input("Stlačte 1 pre spustenie debug módu\n\t\talebo inú klávesu pre normálny mód:  ")
    if debug == "1":
        debug = True
    else:
        debug = False

    start_time = time.time()
    done = iterative_dfs(debug, file_path, max_depth)
    end_time = time.time()
    if done == 1:
        counter = 0
        for crossroad in visited:
            if 0 < counter < len(visited):
                print("\n{}. move".format(counter))
                print_operators(visited[counter - 1], visited[counter])
            else:
                print("\nStarting crossroad:")
            print_crossroad(crossroad)
            counter += 1
    else:
        print("No resolution found.")
    print("\nCompilation time: {}".format(datetime.timedelta(seconds=round(end_time - start_time, 0))))


start()
