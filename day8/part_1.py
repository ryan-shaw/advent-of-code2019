
with open('input.txt', 'r') as f:
    image = f.read()

height = 6
width = 25

image = [int(x) for x in image]
layers = len(image) // (height * width)

min_zero_count = None
solution_layer = None
for _ in range(layers):
    zero_count = 0
    layer = []
    for x in range(height):
        row = []
        for _ in range(width):
            pixel = image.pop(0)
            if pixel == 0:
                zero_count += 1
            row.append(pixel)
        layer.append(row)
    if min_zero_count is None:
        min_zero_count = zero_count
        solution_layer = layer
    elif zero_count < min_zero_count:
        min_zero_count = zero_count
        solution_layer = layer

digit_map = {}
for layer in solution_layer:
    for pixel in layer:
        if pixel in digit_map:
            digit_map[pixel] += 1
        else:
            digit_map[pixel] = 1
print(digit_map[1] * digit_map[2])

