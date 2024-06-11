import copy
# directions
# 0 up
# 1 right
# 2 down
# 3 left

class reflector_tile:
    def __init__(self, symbol) -> None:
        self.symbol = symbol
        self.light = {
            0: False,
            1: False,
            2: False,
            3: False
        }

    def is_energised(self) -> bool:
        return any(self.light[i] for i in range(4))
    
    # for debugging
    def __repr__(self):
        if not self.is_energised() or not self.symbol == '.':
            return self.symbol
        
        light_num = sum(1 if self.light[i] else 0 for i in range(4))

        if light_num > 1:
            return str(light_num)
        
        if self.light[0]:
            return '^'
        
        if self.light[1]:
            return '>'
        
        if self.light[2]:
            return 'v'

        return '<'
    
def get_potential_next_states(symbol, light_dir, x, y):
    if symbol == '.':
        x1, y1 = step(x, y, light_dir)
        return [(x1, y1, light_dir)]
    
    if symbol == '\\':
        next_dir = None

        if light_dir == 0:
            next_dir = 3

        if light_dir == 1:
            next_dir = 2

        if light_dir == 2:
            next_dir = 1

        if light_dir == 3:
            next_dir = 0

        x1, y1 = step(x, y, next_dir)
        return [(x1, y1, next_dir)]
        
    if symbol == '/':
        next_dir = None

        if light_dir == 0:
            next_dir = 1

        if light_dir == 1:
            next_dir = 0

        if light_dir == 2:
            next_dir = 3

        if light_dir == 3:
            next_dir = 2

        x1, y1 = step(x, y, next_dir)
        return [(x1, y1, next_dir)]

    if symbol == '|':
        if light_dir == 0 or light_dir == 2:
            x1, y1 = step(x, y, light_dir)
            return [(x1, y1, light_dir)]

        x1, y1 = step(x, y, 0)
        x2, y2 = step(x, y, 2)
        return [(x1, y1, 0), (x2, y2, 2)]

    # symbol == '-'
    if light_dir == 1 or light_dir == 3:
        x1, y1 = step(x, y, light_dir)
        return [(x1, y1, light_dir)]

    x1, y1 = step(x, y, 1)
    x2, y2 = step(x, y, 3)
    return [(x1, y1, 1), (x2, y2, 3)]

contraption: [[reflector_tile]] = []

with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        contraption.append([])

        for symbol in line.strip():
            contraption[-1].append(reflector_tile(symbol))

len_x = len(contraption[0])
len_y = len(contraption)

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

# (x, y, light)
queue = [(0, 0, 1)]

while len(queue) > 0:
    x, y, light_dir = queue.pop()
    tile = contraption[y][x]
    potential_states = []

    if tile.light[light_dir]:
        # we've been here before
        continue

    tile.light[light_dir] = True

    potential_states = get_potential_next_states(tile.symbol, light_dir, x, y)

    for state in potential_states:
        (state_x, state_y, state_dir) = state

        if in_range(state_x, state_y):
            queue.append(state)

for row in contraption:
    print(row, sep=' ')

for row in contraption:
    print(['#' if tile.is_energised() else '.' for tile in row], sep=' ')

part1_result = sum(sum(1 if tile.is_energised() else 0 for tile in row) for row in contraption)
print('part 1 result: ', part1_result)