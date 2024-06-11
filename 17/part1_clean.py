from sortedcontainers import SortedList

# input

heat_map = []

with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        heat_map.append([int(c) for c in line.strip()])

# preliminaries

len_x = len(heat_map[0])
len_y = len(heat_map)

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
    
class Crucible_Search_State:
    def __init__(self, x, y, heat_loss, forbidden_dir):
        self.x = x
        self.y = y
        self.heat_loss = heat_loss
        self.forbidden_dir = forbidden_dir

# computation

day1_result = None
start_state = Crucible_Search_State(0, 0, 0, None)
queue = SortedList([start_state], key=lambda x: x.heat_loss)
visited_map = [[[False, False] for x in row] for row in heat_map]

while(len(queue) > 0):
    state = queue.pop(0)

    if not state.forbidden_dir is None:
        if visited_map[state.y][state.x][state.forbidden_dir]:
            continue

        visited_map[state.y][state.x][state.forbidden_dir] = True

    if (state.x == len_x - 1) and (state.y == len_y - 1):
        day1_result = state.heat_loss
        break

    for direction in range(4):
        if direction % 2 == state.forbidden_dir:
            continue
    
        (x, y, heat_loss) = (state.x, state.y, state.heat_loss)

        for steps in range(1, 4):
            (x, y) = step(x, y, direction)

            if not in_range(x, y):
                break

            heat_loss += heat_map[y][x]

            if not visited_map[y][x][direction % 2]:
                queue.add(Crucible_Search_State(x, y, heat_loss, direction % 2))

print('day 1 result: ', day1_result)