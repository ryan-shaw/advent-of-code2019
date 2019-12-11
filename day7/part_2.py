#!/usr/bin/env python3

from itertools import permutations

OP_ADD = 1
OP_MULTIPLY = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_JUMP_TRUE = 5
OP_JUMP_FALSE = 6
OP_LT = 7
OP_EQ = 8

ARG_POSITION = 0
ARG_IMMEDIATE = 1

def get_input():
    with open('input.txt', 'r') as f:
        return list(map(lambda x : int(x), f.readline().split(',')))

program = get_input()

class Intcode(object):
    def __init__(self, program, inputs):
        self.program = program
        self.offset = 0
        self.inputs = inputs
        self.outputs = []

    def next(self):
        self.offset += 1
        return self.program[self.offset - 1]

    def get_arg(self, mode = ARG_POSITION):
        if mode == ARG_IMMEDIATE:
            return self.next()
        pos = self.next()
        return self.program[pos]

    def store(self, value):
        pos = self.next()
        # print('Storing {} at {}'.format(value, pos))
        self.program[pos] = value

    def add(self, arg_modes):
        arg0 = self.get_arg(arg_modes[0])
        arg1 = self.get_arg(arg_modes[1])
        res = arg0 + arg1
        # print('[{}] Adding {} + {} = {}'.format(self.offset - 2, arg0, arg1, res))
        self.store(res)

    def multiply(self, arg_modes):
        arg0 = self.get_arg(arg_modes[0])
        arg1 = self.get_arg(arg_modes[1])
        res = arg0 * arg1
        # print('[{}] Multiply {} * {} = {}'.format(self.offset - 2, arg0, arg1, res))
        self.store(res)

    def jump(self, arg_modes, mode):
        res = self.get_arg(arg_modes[0])
        if bool(res) is mode:
            new_offset = self.get_arg(arg_modes[1])
            # print('[{}] Jumping to {} because {}'.format(self.offset, new_offset, res))
            # self.offset = self.get_arg(arg_modes[1])
            self.offset = new_offset
        else:
            self.offset += 1

    def lt(self, arg_modes):
        arg1 = self.get_arg(arg_modes[0])
        arg2 = self.get_arg(arg_modes[1])
        self.program[self.next()] = 1 if arg1 < arg2 else 0

    def eq(self, arg_modes):
        arg1 = self.get_arg(arg_modes[0])
        arg2 = self.get_arg(arg_modes[1])
        self.program[self.next()] = 1 if arg1 == arg2 else 0

    def print(self, arg_modes):
        res = self.get_arg(arg_modes[0])
        # print('Outputting {}'.format(res))
        self.outputs.append(res)

    def resume(self):
        self.suspended = False
        # print(self.inputs)
        return self.process()
    
    def suspend(self):
        self.suspended = True

    def process(self):
        instruction = self.next()
        z = str(instruction)[:-2].zfill(3)
        arg_modes = ([int(x) for x in z])[::-1]
        opcode = (int(str(instruction)[-2:]))
        if opcode == OP_ADD:
            self.add(arg_modes)
        elif opcode == OP_MULTIPLY:
            self.multiply(arg_modes)
        elif opcode == OP_JUMP_TRUE:
            self.jump(arg_modes, True)
        elif opcode == OP_JUMP_FALSE:
            self.jump(arg_modes, False)
        elif opcode == OP_LT:
            self.lt(arg_modes)
        elif opcode == OP_EQ:
            self.eq(arg_modes)
        elif opcode == 99:
            # print('exit')
            return True
        elif opcode == OP_INPUT:
            if not self.inputs:
                # suspend program
                print('Suspended waiting input pos', self.offset)
                self.suspend()
                return 
            # print(self.inputs)
            res = self.inputs.pop(0)
            pos = self.next()
            self.program[pos] = int(res)
        elif opcode == OP_OUTPUT:
            self.print(arg_modes)
            # print('Suspended waiting input pos', self.offset)
            return
        else:
            raise Exception('opcode not known {} pos {}'.format(opcode, self.offset))
        # print(self.program, self.offset + 1)
        return self.process()

def get_inputs():
    start = 5
    end = 10
    return permutations(range(start, end))

max_result = 0
solution = None
for inputs in get_inputs():
    print(inputs)
    prev_out = 0
    programs = {}
    running = True
    count = 0
    while running:
        for idx, i in enumerate(inputs):
            # print('Index: ', idx)
            code = programs.get(idx)
            if not code:
                code = Intcode(program.copy(), [i, prev_out])
                running = not code.process()
                # if idx == 0:
                # print(code.program, idx)
            else:
                # print(prev_out, code.offset)
                code.inputs.append(prev_out)
                # if idx == 0:
                # print(code.program, idx)
                running = not code.resume()
            programs[idx] = code
            if not running:
                print(inputs, code.inputs)
                if code.inputs[0] > max_result:
                    max_result = code.inputs[0]
                    solution = inputs
                break
            prev_out = code.outputs[-1]
        if not running:
            break
print(max_result, solution)
