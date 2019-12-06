#!/usr/bin/env python3

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
    def __init__(self, program):
        self.program = program
        self.offset = 0

    def next(self):
        self.offset += 1
        return self.program[self.offset - 1]

    def get_arg(self, mode = ARG_POSITION):
        if mode == ARG_IMMEDIATE:
            return self.next()
        pos = self.next()
        return self.program[pos]

    def output(self, value):
        pos = self.next()
        self.program[pos] = value

    def add(self, arg_modes):
        res = self.get_arg(arg_modes[0]) + self.get_arg(arg_modes[1])
        self.output(res)

    def multiply(self, arg_modes):
        res = self.get_arg(arg_modes[0]) * self.get_arg(arg_modes[1])
        self.output(res)

    def jump(self, arg_modes, mode):
        res = self.get_arg(arg_modes[0])
        if bool(res) is mode:
            self.offset = self.get_arg(arg_modes[1])
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
        print(res)

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
            return
        elif opcode == OP_INPUT:
            res = input('Input please')
            pos = self.next()
            program[pos] = int(res)
        elif opcode == OP_OUTPUT:
            self.print(arg_modes)
        else:
            print(self.offset)
            raise Exception('opcode not known {}'.format(opcode))
        self.process()

p = Intcode(program)
p.process()
