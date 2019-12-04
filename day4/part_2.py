#!/usr/bin/env python3

# It is a six-digit number.
# The value is within the range given in your puzzle input.
# Two adjacent digits are the same (like 22 in 122345).
# Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

# 111111 meets these criteria (double 11, never decreases).
# 223450 does not meet these criteria (decreasing pair of digits 50).
# 123789 does not meet these criteria (no double).

# An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.

# 112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
# 123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
# 111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).

input_range = [273025, 767253]

def check(val):
    # Check adjacent
    s = str(val)
    found = False
    adjacent_list = []
    for x in range(len(s)):
        digit = s[x]
        if x+1 < len(s):
            if s[x] == s[x+1]:
                found = True
            if s[x+1] < s[x]:
                found = False
                break
        if not adjacent_list:
            adjacent_list.append({digit: 1})
            continue
        key = list(adjacent_list[-1].keys())[0]
        if key == digit:
            adjacent_list[-1][key] += 1
        else:
            adjacent_list.append({digit: 1})
        
        if x+1 >= len(s): continue
        if s[x] == s[x+1]:
            found = True
        if s[x+1] < s[x]:
            found = False
            break
    if found:
        for item in adjacent_list:
            if item[list(item.keys())[0]] == 2:
                return True
    return False

if __name__ == "__main__":
    count = 0
    for x in range(input_range[0], input_range[1]):
        found = check(x)
        if found: count += 1
    print('Solution: {}'.format(count))