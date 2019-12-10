from math import gcd, atan2
import collections

def get_asteroids():
    asteroids = []
    with open('input.txt') as f:
        for y, line in enumerate(f.readlines()):
            for x, c in enumerate(line.strip()):
                if c == '#':
                    asteroids.append((x, y))
    return asteroids

asteroids = get_asteroids()

def get_visible(site):
    detected = set()
    for asteroid in asteroids:
        if asteroid == site: continue
        dx, dy = asteroid[0] - site[0], asteroid[1] - site[1]
        d = abs(gcd(dx, dy))
        r = (dx//d, dy//d)
        detected.add(r)
    return detected

siteCounts = []
for site in asteroids:
    visible = get_visible(site)
    siteCounts.append((len(visible), site, visible))

    siteCounts.sort(reverse=True)
    amt, site, visible = siteCounts[0]
print(amt)

# sorted by angle then distance
destroyed = [(atan2(dx, dy), (dx, dy)) for dx, dy in visible]
destroyed.sort(reverse=True)

# for d in destroyed: print(round(d[0], 3))
print(destroyed[199][1], site)
dx, dy = destroyed[200-1][1]

x, y = site[0] + dx, site[1] + dy
# get back from divided to actual coords
while (x, y) not in asteroids:
    x, y = x+dx, y+dy
print("Part 2: {}".format((x*100) + y))
