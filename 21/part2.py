import copy
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

def positions(steps: int) -> int:
    possible_positions = set()
    possible_positions.add((start_x, start_y))

    for i in range(steps):
        next = set()

        for pos in possible_positions:
            (x, y) = pos

            for direction in range(4):
                (x_next, y_next) = step(x, y, direction)

                if in_range(x_next, y_next) and garden[y_next][x_next] != '#':
                    next.add((x_next, y_next))

        possible_positions = next

    #test_garden = copy.deepcopy(garden)

    #print('+++++++++++++++++++++++++++++++')

    #for (x, y) in possible_positions:
    #    test_garden[y][x] = 'O'
    #
    #for row in test_garden:
    #    print(''.join(row))

    return len(possible_positions)

steps = 26501365
day2_result = 0

positions_middle_even = positions(64)
positions_middle_odd = positions(65)

positions_total_even = positions(132)
positions_total_odd = positions(133)

positions_outside_even = positions_total_even - positions_middle_even
positions_outside_odd = positions_total_odd - positions_middle_odd

multiplicity = steps // len_x

for i in range(1, multiplicity):
    if i % 2 == 0:
        day2_result += i * 4 * positions_total_odd

    if i % 2 == 1:
        day2_result += i * 4 * positions_total_even

#if multiplicity % 2 == 0:
day2_result += multiplicity * positions_outside_even
day2_result += 4 * multiplicity * positions_total_odd - 2 * positions_outside_odd - (multiplicity - 1) * positions_outside_odd
#else:
#    day2_result += 4 * (multiplicity + 1) * positions_middle_odd + 2 * positions_outside_odd + 3 * multiplicity * positions_outside_odd

# center garden
day2_result += positions_total_odd

print('day 2 result: ', day2_result)
print(multiplicity)
print(steps % len_x)