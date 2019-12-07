#!/usr/bin/env python3

def get_input():
    with open('./input.txt') as f:
        return (x.rstrip().split(')') for x in f.readlines())

inputs = get_input()
# graph = {'COM': ['B'], 'B': ['C', 'D']}
graph = {}

def find_path(start, target, path=[]):
    path = path + [start]
    if start == target:
        return path
    if start not in graph:
        return None
    # print(graph)
    for node in graph[start]:
        newpath = find_path(node, target, path)
        if newpath:
            return newpath

def find_all_paths(start, path=[]):
    path = path + [start]
    paths = []
    if start not in graph:
        return path
    for node in graph[start]:
        newpaths = find_all_paths(node, path)
    
    return paths

def count_leaves(_start):
    counts = []
    def _count(start, path = [], count = 0):
        path = path + [start]
        if start not in graph:
            return count
        for node in graph[start]:
            c = _count(node, path, count + 1)
            counts.append(c)
        return count
    _count(_start)
    return sum(counts)

def find_shortest_path(start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

def add_child(parent, child):
    if parent not in graph:
        graph[parent] = [child]
    else:
        graph[parent].append(child)

for i in inputs:
    # Add child
    add_child(i[0], i[1])

# print(count_leaves('COM'))
# print(graph)
# print(find_shortest_path('K', 'I'))
san_path = find_path('COM', 'SAN')
you_path = find_path('COM', 'YOU')

# print(san_path, you_path)

# ['COM', 'B', 'C', 'D', 'I', 'SAN'] ['COM', 'B', 'C', 'D', 'E', 'J', 'K', 'YOU']

# findn common ancestor 
common = None
for key in san_path[::-1]:
    if key not in you_path:
        pass
    elif not common:
        common = key
# print(common)
# print(len(you_path) - you_path.index(common) - 2)
solution = (len(you_path) - you_path.index(common) - 2) + (len(san_path) - san_path.index(common) - 2)
print(solution)


# for i in inputs:
#     # print(i)
#     res = find_path('COM', i[0])
#     print(res)
#     if not res:
        # graph[i[0]] = [i[1]]
    # else:
    #     graph[i[0]].append(i[1])
# print(graph)
# print(find_all_paths('COM'))
