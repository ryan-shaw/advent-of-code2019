#!/usr/bin/env python3
from sys import stdout
from aoc import timer
from intcode import Intcode

def get_input():
    with open('inputs/input11', 'r') as f:
        return list(map(lambda x : int(x), f.readline().split(',')))

program = get_input()

@timer
def solve():
    x, y, max_x, max_y, min_x, min_y = 0, 0, 0, 0, 0, 0
    # 0 right, 1 down, 2 left, 3 up
    direction = 3
    panels = {}
    exited = False
    p = Intcode(program, [])
    while not exited:
        i = panels.get((x, y), [1])[-1]
        p.inputs.append(i)
        exited = not p.resume()
        colour = p.outputs.pop(0)
        rotate = p.outputs.pop(0)
        if (x, y) in panels:
            panels[(x, y)].append(colour)
        else:
            panels[(x, y)] = [colour]
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        direction = (direction + [-1, 1][rotate]) % 4
        if direction == 0:
            x += 1
        elif direction == 1:
            y -= 1
        elif direction == 2:
            x -= 1
        elif direction == 3:
            y += 1

    print('Panel count', len(panels))

    offset_y = min_y
    offset_x = min_x


    for y in range(max_y + abs(offset_y), -1, -1):
        for x in range(0, max_x + abs(offset_x)):
            p = panels.get((x + offset_x, y + offset_y), [0])[0]
            if p == 0: stdout.write("⬛️")
            else: stdout.write("⬜️")
        print()
            
solve()
