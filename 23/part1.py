import itertools

map = []

arrow_dict = {
    '^' : 0, 
    '>' : 1, 
    'v' : 2, 
    '<' : 3
    }

arrows = list(arrow_dict.keys())

with open('C:\\Users\\Lenovo\\source\\repos\\AdventOfCode23\\23\\input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        map.append([c for c in line.strip()])

#for row in map:
#    print(' '.join(row))

start_x = map[0].index('.')
end_x = map[-1].index('.')

len_x = len(map[0])
len_y = len(map)

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
    
class Mountain_Map_Node:
    def __init__(self, pos):
        self.pos = pos
        self.destinations = []
        self.traverse_length = []

    def connect(self, neighbour, length):
        self.destinations.append(neighbour)
        self.traverse_length.append(length)

class Mountain_Search_State:
    def __init__(self, path, length):
        self.path = path
        self.length = length

def get_options(p) -> list[(int, int)]:
    global map

    (x, y) = p
    stand = map[y][x]

    if stand == '#':
        return []

    if stand in arrows:
        directions = [arrow_dict[stand]]
    else:
        directions = range(4)

    options = []
    for direction in directions:
        (x1, y1) = step(x, y, direction)

        if (not in_range(x1, y1)) or (map[y1][x1] == '#'):
            continue

        options.append((x1, y1))

    return options

crossroads = [p for p in itertools.product(range(len_y), range(len_x)) if len(get_options(p)) > 2]

start_node = Mountain_Map_Node((start_x, 0))
end_node = Mountain_Map_Node((end_x, len_y - 1))

map_nodes = [Mountain_Map_Node(pos) for pos in crossroads] + [start_node, end_node]

for node in map_nodes:
    pos = node.pos

    for path_start in get_options(pos):
        last_position = pos
        current_position = path_start
        length = 1

        while True:

            if any(True for n in map_nodes if n.pos == current_position):
                # found another crossroad
                other_node = next(n for n in map_nodes if n.pos == current_position)
                node.connect(other_node, length)
                #print('connect node', node.pos, 'to', other_node.pos, 'with length', length, sep=' ')
                break

            next_options = [o for o in get_options(current_position) if not o == last_position]

            if len(next_options) == 0:
                # dead-end
                #print('found dead end at ', current_position)
                break

            length += 1
            last_position = current_position
            current_position = next_options[0]

start_state = Mountain_Search_State([start_node], 0)
queue = [start_state]
day2_result = None

while len(queue) > 0:
    state = queue.pop()
    node = state.path[-1]

    if node == end_node:
        if day2_result is None or state.length > day2_result:
            day2_result = state.length
            continue

    for i, destination in enumerate(node.destinations):
        if destination in state.path:
            continue

        traverse_length = node.traverse_length[i]
        queue.append(Mountain_Search_State(state.path + [destination], state.length + traverse_length))

print('day 2 result: ', day2_result)