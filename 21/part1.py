garden = []
(start_x, start_y) = (None, None)

with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        if 'S' in line:
            start_y = len(garden)
            start_x = line.index('S')

        garden.append([c for c in line.strip()])

len_x = len(garden[0])
len_y = len(garden)

def in_range(x, y) -> bool:
    return 0 <= x and x < len_x and 0 <= y and y < len_y

def step(x, y, dir) -> (int, int):
    if dir == 0:
        # up
        return (x, y - 1)
    
    if dir == 1:
        # right
        return (x + 1, y)
    
    if dir == 2:
        #down
        return (x, y + 1)
    
    if dir == 3:
        #left
        return (x - 1, y)
    
possible_positions = set()
possible_positions.add((start_x, start_y))

for i in range(64):
    next = set()

    for pos in possible_positions:
        (x, y) = pos

        for direction in range(4):
            (x_next, y_next) = step(x, y, direction)

            if in_range(x_next, y_next) and garden[y_next][x_next] != '#':
                next.add((x_next, y_next))

    possible_positions = next

part1_result = len(possible_positions)
print('part 1 result: ', part1_result)

for (x, y) in possible_positions:
    garden[y][x] = 'O'

for row in garden:
    print(''.join(row))