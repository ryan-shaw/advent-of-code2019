import re
import matplotlib.pyplot as plt 
from aoc import timer
from collections import namedtuple
from itertools import permutations, combinations

Polar = namedtuple('Polar', 'x y z')

class Polar(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'<x={self.x} y={self.y}, z={self.z}>'

class Moon(object):
    def __init__(self, x, y, z):
        self.pos = Polar(x, y, z)
        self.velocity = Polar(0, 0, 0)

    def __repr__(self):
        return f'{{pos={self.pos}, vel={self.velocity}}}'

    @staticmethod
    def parse_moon(pos):
        rex = re.compile(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>')
        m = rex.match(pos)

        return Moon(int(m.group(1)), int(m.group(2)), int(m.group(3)))

def get_input():
    with open('inputs/input12', 'r') as f:
        return [Moon.parse_moon(x) for x in f.readlines()]

def apply_gravity(moons):
    c = 0
    for moon, other in combinations(moons, 2):
        for axis in ['x', 'y', 'z']:
            value = getattr(moon.pos, axis)
            value_other = getattr(other.pos, axis)
            change = 0
            if value > value_other:
                change = -1
            elif value < value_other:
                change = 1
            setattr(moon.velocity, axis, getattr(moon.velocity, axis) + change)
            setattr(other.velocity, axis, getattr(other.velocity, axis) + -change)
    
    for moon in moons:
        moon.pos.x += moon.velocity.x
        moon.pos.y += moon.velocity.y
        moon.pos.z += moon.velocity.z

def calc_energy(moons):
    energy_sum = 0
    for moon in moons:
        pot = abs(moon.pos.x) + abs(moon.pos.y) + abs(moon.pos.z)
        kin = abs(moon.velocity.x) + abs(moon.velocity.y) + abs(moon.velocity.z)
        total = pot * kin
        energy_sum += total
    return energy_sum

def gcd(a,b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a
    
def compute_lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b / gcd(a, b)

@timer
def solve():
    steps = 10000000000000
    moons = get_input()
    print('After 0 steps:')
    initial_state_x = [(moon.pos.x, moon.velocity.x) for moon in moons]
    initial_state_y = [(moon.pos.y, moon.velocity.y) for moon in moons]
    initial_state_z = [(moon.pos.z, moon.velocity.z) for moon in moons]
    ys = {'x': [], 'y': [], 'z': []}
    xs = []
    initial_state = [str(x) for x in moons]
    freq_x = 0
    freq_y = 0
    freq_z = 0
    # for i in moons:
    #     print(i)
    for x in range(steps):
        xs.append(x)
        # print('After {} steps:'.format(x+1))
        apply_gravity(moons)
        # for i in moons:
        #     print(i)

        cmpx = [(moon.pos.x, moon.velocity.x) for moon in moons]
        cmpy = [(moon.pos.y, moon.velocity.y) for moon in moons]
        cmpz = [(moon.pos.z, moon.velocity.z) for moon in moons]
        if not freq_x and cmpx == initial_state_x:
            freq_x = x + 1
        if not freq_y and cmpy == initial_state_y:
            freq_y = x + 1
        if not freq_z and cmpz == initial_state_z:
            freq_z = x + 1
        if freq_x and freq_y and freq_z:
            print(freq_x, freq_y, freq_z)
            print('Found frequencies')
            break
    energy = calc_energy(moons)
    lcm = compute_lcm(freq_x, freq_y)
    print(compute_lcm(lcm, freq_z))
solve()
