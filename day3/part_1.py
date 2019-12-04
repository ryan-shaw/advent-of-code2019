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
            for _ in range(travel):
                y += 1
                self.mark(x, y, steps + 1)
        elif direction == 'R':
            for _ in range(travel):
                x += 1
                self.mark(x, y, steps + 1)
        elif direction == 'D':
            for _ in range(travel):
                y -= 1
                self.mark(x, y, steps + 1)
        elif direction == 'L':
            for _ in range(travel):
                x -= 1
                self.mark(x, y, steps + 1)
        else:
            raise Exception('invalid direction {}'.format(direction))

        if code:
            self.create(code, x, y, steps + 1)

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

    distances = []

    for key1, value1 in wire1.marked.items():
        for key2, _ in value1.items():
            exists = wire2.marked.get(key1, {}).get(key2)
            if exists:
                distance = abs(key1) + abs(key2)
                print('Distance: {}'.format(distance))
                distances.append(distance)
    
    print('Solution: {}'.format(min(distances)))
