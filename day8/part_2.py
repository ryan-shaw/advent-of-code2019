from sys import stdout

with open('input.txt', 'r') as f:
    image = f.read()

height = 6
width = 25
# height = 2
# width = 2

image = [int(x) for x in image]
layers = len(image) // (height * width)

layer_list = []
for _ in range(layers):
    zero_count = 0
    layer = []
    for x in range(height):
        row = []
        for _ in range(width):
            pixel = image.pop(0)
            row.append(pixel)
        layer.append(row)
    layer_list.append(layer)
# print(layer_list)


# loop through each row in each layer
image = {}
for y in range(height):
    for x in range(width):
        for layer in layer_list:
            # print(y, x, layer[y][x])
            key = (y, x)
            if key in image:
                currval = image[key] 
                if currval == 2:
                    image[key] = layer[y][x]
            else:
                image[key] = layer[y][x]

# for values in image.values():
#     print(values)

# print(image)
# solution = ''.join([str(x) for x in image.values()])
solution = list(image.values())
# # solution = solution.replace('1', '\x1b[6;30;42m 1\x1b[0m')
y1 = [ solution[i:i+width] for i in range(0, len(solution), width) ]
for line in y1:
    for digit in line:
        if digit == 0: stdout.write("⬛️")
        else: stdout.write("⬜️")
    print()
# for s in y1:
#     print(','.join(s))
