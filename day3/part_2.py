#!/usr/bin/env python3

import functools 

class Wire():

    def __init__(self):
        self.marked = {}

    def mark(self, x, y, steps):
        existing = self.marked.get(x)
        if existing is None:
            self.marked[x] = {}
        self.marked[x][y] = steps

    def create(self, code, x, y, steps = 0):
        move = code.pop(0)
        direction = move[0]
        travel = int(move[1:])
        if direction == 'U':
            for step in range(travel):
                y += 1
                self.mark(x, y, steps + step + 1)
            steps += travel
        elif direction == 'R':
            for step in range(travel):
                x += 1
                self.mark(x, y, steps + step + 1)
            steps += travel
        elif direction == 'D':
            for step in range(travel):
                y -= 1
                self.mark(x, y, steps + step + 1)
            steps += travel
        elif direction == 'L':
            for step in range(travel):
                x -= 1
                self.mark(x, y, steps + step + 1)
            steps += travel
        else:
            raise Exception('invalid direction {}'.format(direction))

        if code:
            self.create(code, x, y, steps)

def load():
    with open('./input.txt', 'r') as f:
        yield f.readline().rstrip()
        yield f.readline().rstrip()

if __name__ == "__main__":
    inputs = load()
    wire1 = Wire()
    wire1.create(next(inputs).split(','), 0, 0)
    wire2 = Wire()
    wire2.create(next(inputs).split(','), 0, 0)

    step_list = []

    for key1, value1 in wire1.marked.items():
        for key2, steps in value1.items():
            steps2 = wire2.marked.get(key1, {}).get(key2)
            if steps2:
                print(steps + steps2, key1, key2)
                step_list.append(steps + steps2)
    # print(wire2.marked)
    
    print('Solution: {}'.format(min(step_list)))
