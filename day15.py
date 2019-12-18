from intcode import Intcode
from aoc import timer, read_program
from collections import defaultdict, deque
from itertools import product

grid = defaultdict(lambda : '?')
robot_x = 0
robot_y = 0
backtrack = deque()
grid[(0,0)] = '.'
steps = 0
paths = {}
minutes = 0
oxygen = None

# moves           = {2: (1, 0), 1: (-1, 0), 4: (0, 1), 3: (0, -1)}
backtrack_moves = {2: (0, -1), 1: (0, 1), 4: (1, 0), 3: (-1, 0)}

def get_input():
    global robot_x, robot_y, steps
    # get not visited positions
    #move right 
    steps += 1
    if grid.get((robot_x + 1, robot_y), 0) == 0:
        # print('moving right')
        robot_x += 1
        backtrack.append(3)
        return 4
    elif grid.get((robot_x - 1, robot_y), 0) == 0:
        # print('moving left')
        robot_x -= 1
        backtrack.append(4)
        return 3
    elif grid.get((robot_x, robot_y + 1), 0) == 0:
        # print('moving up')
        robot_y += 1
        backtrack.append(2)
        return 1
    elif grid.get((robot_x, robot_y - 1), 0) == 0:
        # print('moving down')
        robot_y -= 1
        backtrack.append(1)
        return 2
    else:
        if not backtrack: return
        back = backtrack.pop() # reverse previous move
        steps -= 2
        if back == 1:
            robot_y += 1
        elif back == 2:
            robot_y -= 1
        elif back == 3:
            robot_x -= 1
        elif back == 4:
            robot_x += 1
        return back

def draw(minutes):
    for y in (range(-20, 22)):
        print(y, '\t', end = '')
        for x in range(-21, 30):
            val = grid.get((x, y), ' ')
            if robot_x == x and robot_y == y:
                val = '0'
            print(val, end='')
        print()
    print('Minutes', minutes - 1)

def process_output(state):
    global robot_x, robot_y, steps, oxygen
    # if state != 0:
    #     move = backtrack[-1]
    #     move = backtrack_moves[move]
    #     steps -= 1
    #     x = robot_x + move[0]
    #     paths.setdefault((x, y), set())
    #     y = robot_y + move[1]
    #     paths[x, y].add((robot_x, robot_y))
    if state == 0:
        grid[(robot_x, robot_y)] = '\u2588'
        move = backtrack.pop()
        move = backtrack_moves[move]
        steps -= 1
        robot_x += move[0]
        robot_y += move[1]
    elif state == 1:
        grid[(robot_x, robot_y)] = '.'
    elif state == 2:
        grid[(robot_x, robot_y)] = '0'
        oxygen = (robot_x, robot_y)
        print('Oxygen at ', robot_x, robot_y)
    else:
        return True

@timer
def part1():
    code = read_program(15)
    p = Intcode(code, [])
    _input = get_input()
    running = True
    while running:
        p.inputs.append(_input)
        p.suspended = False
        running = p.run()
        done = process_output(p.outputs.pop(0))
        if done: break
        # draw(0)
        _input = get_input()
        if _input is None: break
    print('Solution:', steps)

part1()

def neighbours(coords):
    p = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for delta in p:
        if delta == (0,0):
            continue
        yield (coords[0] + delta[0], coords[1] + delta[1])


@timer
def part2():
    global minutes, grid, oxygen
#     g = """###### 
# #..### 
# #.#..#
# #.O.##
# #####""".split('\n')
#     x = 0
#     y = 0
#     grid = defaultdict(lambda : '#')
#     for l in g:
#         for cell in l.strip():
#             grid[(x, y)] = cell
#             print(cell)
#             x += 1
#         y += 1
#         x = 0
#     print(grid)
#     robot_x = 2
#     robot_y = 3

    minutes = 1
    pos = oxygen
    done = {pos}
    oxygen = [pos]
    while oxygen:
        void = []
        for coords in oxygen:
            # get neighbours
            for cell in neighbours(coords):
                if cell in done:
                    continue
                if grid[cell] != '.':
                    continue
                # print(cell)
                grid[cell] = minutes % 10
                # grid[cell] = 'O'
                # print('O', cell)
                # import time
                # time.sleep(0.3)
                done.add(cell)
                void.append(cell)
        oxygen = void
        # print(void)
        minutes += 1
        draw(minutes)
    print(minutes - 2)
part2()
