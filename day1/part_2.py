#!/usr/bin/env python3

def get_input():
    with open('./input.txt', 'r') as f:
        return f.readlines()

def calc_fuel_total(mass):
    remain = (mass // 3) - 2
    if remain > 0:
        remain += calc_fuel_total(remain)
    elif remain <= 0:
        return 0
    return remain


if __name__ == "__main__":
    sum = 0
    masses = get_input()
    for mass in masses:
        calced = calc_fuel_total(int(mass.rstrip()))
        # print(calced)
        sum += calced

    print(sum)
