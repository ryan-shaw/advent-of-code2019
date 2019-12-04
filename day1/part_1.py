#!/usr/bin/env python3

def get_input():
    with open('./input.txt', 'r') as f:
        return f.readlines()

def calc_fuel(mass):
    return (mass // 3) - 2

if __name__ == "__main__":
    sum = 0
    for line in get_input():
        fuel = calc_fuel(int(line.rstrip()))
        sum += fuel
    print(sum)
