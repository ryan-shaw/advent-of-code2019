#!/usr/bin/env python3

# It is a six-digit number.
# The value is within the range given in your puzzle input.
# Two adjacent digits are the same (like 22 in 122345).
# Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

# 111111 meets these criteria (double 11, never decreases).
# 223450 does not meet these criteria (decreasing pair of digits 50).
# 123789 does not meet these criteria (no double).

input_range = [273025, 767253]

def check(val):
    # Check adjacent
    s = str(val)
    found = False
    for x in range(len(s)):
        if x+1 >= len(s): continue
        if s[x] == s[x+1]:
            found = True
        if s[x+1] < s[x]:
            found = False
            break
    return found

if __name__ == "__main__":
    count = 0
    for x in range(input_range[0], input_range[1]):
        found = check(x)
        if found:
            count += 1
    print('Solution: {}'.format(count))