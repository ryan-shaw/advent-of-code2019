
OP_ADD = 1
OP_MULTIPLY = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_JUMP_TRUE = 5
OP_JUMP_FALSE = 6
OP_LT = 7
OP_EQ = 8
OP_REL_BASE_OFF = 9

ARG_POSITION = 0
ARG_IMMEDIATE = 1
ARG_RELATIVE = 2

class Intcode(object):
    def __init__(self, program, inputs):
        self.program = program
        self.offset = 0
        self.inputs = inputs
        self.outputs = []
        self.relative_base = 0
        self.suspended = False

    def next(self):
        self.offset += 1
        return self.program[self.offset - 1]

    def get_arg(self, mode = ARG_POSITION):
        if mode == ARG_IMMEDIATE:
            return self.next()
        elif mode == ARG_POSITION:
            pos = self.next()
            if pos >= len(self.program):
                return 0
            return self.program[pos]
        elif mode == ARG_RELATIVE:
            arg = self.next()
            pos = self.relative_base + arg
            return self.program[pos]
        else:
            raise Exception('invalid arg param')

    def store_at(self, value, pos):
        if pos >= len(self.program):
            self.program = self.program[:pos+1] + [0]*(pos + 1 - len(self.program))
        self.program[pos] = value

    def store(self, value, arg_mode):
        pos = self.next()
        if arg_mode == ARG_POSITION:
            self.store_at(value, pos)
        elif arg_mode == ARG_RELATIVE:
            self.store_at(value, self.relative_base + pos)
        else:
            raise Exception('invalid store mode')

    def add(self, arg_modes):
        arg0 = self.get_arg(arg_modes[0])
        arg1 = self.get_arg(arg_modes[1])
        res = arg0 + arg1
        # print('[{}] Adding {} + {} = {}'.format(self.offset - 2, arg0, arg1, res))
        self.store(res, arg_modes[2])

    def multiply(self, arg_modes):
        arg0 = self.get_arg(arg_modes[0])
        arg1 = self.get_arg(arg_modes[1])
        res = arg0 * arg1
        # print('[{}] Multiply {} * {} = {}'.format(self.offset - 2, arg0, arg1, res))
        self.store(res, arg_modes[2])

    def jump(self, arg_modes, mode):
        res = self.get_arg(arg_modes[0])
        if bool(res) is mode:
            self.offset = self.get_arg(arg_modes[1])
        else:
            self.offset += 1

    def lt(self, arg_modes):
        arg1 = self.get_arg(arg_modes[0])
        arg2 = self.get_arg(arg_modes[1])
        # self.program[self.next()] = 1 if arg1 < arg2 else 0
        self.store(1 if arg1 < arg2 else 0, arg_modes[2])

    def eq(self, arg_modes):
        arg1 = self.get_arg(arg_modes[0])
        arg2 = self.get_arg(arg_modes[1])
        # self.program[self.next()] = 1 if arg1 == arg2 else 0
        self.store(1 if arg1 == arg2 else 0, arg_modes[2])

    def output(self, arg_modes):
        res = self.get_arg(arg_modes[0])
        self.outputs.append(res)

    def resume(self):
        self.suspended = False
        return self.run()
    
    def suspend(self):
        self.suspended = True

    def run(self):
        running = True
        while running:
            running = self.process()
            if self.suspended:
                return True
        return False

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
            return False
        elif opcode == OP_INPUT:
            if not self.inputs:
                # suspend program
                self.offset -= 1
                self.suspend()
                return True
            res = self.inputs.pop(0)
            pos = self.next()
            if arg_modes[0] == ARG_RELATIVE:
                pos = self.relative_base + pos
            self.store_at(res, pos)
        elif opcode == OP_OUTPUT:
            self.output(arg_modes)
        elif opcode == OP_REL_BASE_OFF:
            arg = self.get_arg(arg_modes[0])
            self.relative_base += arg
        else:
            raise Exception('opcode not known {} pos {}'.format(opcode, self.offset))
        return True
