import time
from sys import stdout
from intcode import Intcode
from os import system
from aoc import timer

def get_input():
    with open('inputs/input13', 'r') as f:
        return list(map(lambda x : int(x), f.readline().split(',')))

program = get_input()

@timer
def part1():
    p = Intcode(program, [])
    p.run()
    f = list(filter(lambda x : x == 2, p.outputs[2::3]))
    print('Part 1:', len(f))

part1()
score = 0
max_x = 36
drawing = {}
max_y = 21
def draw(p):
    global score, drawing, max_x, max_y
    j = 0
    # print('Output count', len(p.outputs))
    while j < len(p.outputs):
        x = p.outputs[j]
        y = p.outputs[j + 1]
        t = p.outputs[j + 2]
        if x == -1:
            score = t
        # max_x = max(max_x, x)
        # max_y = max(max_y, y)
        drawing[(x, y)] = t
        j += 3
    ball = None
    paddle = None
    # system('clear')
    for y in range(0, max_y):
        for x in range(0, max_x + 1):
            t = drawing[(x, y)]
            if t == 1:
                pass
                # stdout.write('|')
            elif t == 2:
                pass
                # stdout.write('#')
            elif t == 3:
                # stdout.write('_')
                paddle = x
            elif t == 4:
                # stdout.write('o')
                ball = x
            elif t == 0:
                pass
                # stdout.write(' ')
        # print()
    if ball > paddle:
        return 1
    elif ball < paddle:
        return -1
    else:
        return 0

@timer
def part2():
    program[0] = 2
    p = Intcode(program, [0])
    wait_input = True
    while wait_input:
        wait_input = p.run()
        i = draw(p)
        del p.outputs[:]
        if wait_input:
            # time.sleep(0.01)
            p.suspended = False
            p.inputs.append(i)

    print('Part 2:', score)

part2()
