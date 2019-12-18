# 10 ORE => 10 A
# 1 ORE => 1 B
# 7 A, 1 B => 1 C
# 7 A, 1 C => 1 D
# 7 A, 1 D => 1 E
# 7 A, 1 E => 1 FUEL

def parse_graph():
    def _p(i):
        num, ele = i.strip().split()
        return ele, int(num)
    reactions = {}
    with open('inputs/input14') as f:
        for line in f.readlines():
            inp, out = line.rstrip().split(' => ')
            left, right = list(map(_p, left.split(','))), _p(right)
            reactions[right[0]] = (right[1], left)
    return reactions

parse_graph()