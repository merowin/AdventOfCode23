from sortedcontainers import SortedList
from termcolor import colored
import os
os.system('color')

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
    def __init__(self, x, y, heat_loss, forbidden_dir, previous):
        self.x = x
        self.y = y
        self.heat_loss = heat_loss
        self.forbidden_dir = forbidden_dir
        self.previous = previous


visited_map = []
for row in heat_map:
    visited_row = []
    for x in row:
        # to remember which search states we've visited already
        visited_row.append([False, False, False, False])

    visited_map.append(visited_row)

# computation

day1_result = None
result_state = None
start_state = Crucible_Search_State(0, 0, 0, None, None)
queue = SortedList([start_state], key=lambda x: x.heat_loss)

while(len(queue) > 0):
    #print(len(queue))
    state = queue.pop(0)
    if not state.forbidden_dir is None:
        if visited_map[state.y][state.x][state.forbidden_dir] == True:
            continue

        visited_map[state.y][state.x][state.forbidden_dir] = True
    #print('******************')
    #print(state.x, state.y, state.heat_loss, state.forbidden_dir, sep=',')

    if (state.x == len_x - 1) and (state.y == len_y - 1):
        day1_result = state.heat_loss
        result_state = state
        break

    for direction in range(4):
        if direction == state.forbidden_dir or (direction + 2) % 4 == state.forbidden_dir:
            continue
    
        (x, y, heat_loss) = (state.x, state.y, state.heat_loss)

        for steps in range(1, 4):
            (x, y) = step(x, y, direction)
            #print('considering point', x, y, sep=' ')
            if not in_range(x, y):
                #print('discarded point outside', x, y, sep=' ')
                break

            heat_loss += heat_map[y][x]

            if not visited_map[y][x][direction] == True:
                queue.add(Crucible_Search_State(x, y, heat_loss, direction, state))
                #print(x, y, heat_loss, direction)
            #else:
                #print('discarded point visited', x, y, sep=' ')

print('day 1 result: ', day1_result)

debug_map = [[str(c) for c in row] for row in heat_map]

debug_state = result_state
while not debug_state.previous is None:
    (x, y, dir) = (debug_state.x, debug_state.y, debug_state.forbidden_dir)

    if dir == 0:
        debug_map[y][x] = '^'
    if dir == 1:
        debug_map[y][x] = '>'
    if dir == 2:
        debug_map[y][x] = 'v'
    if dir == 3:
        debug_map[y][x] = '<'

    (prev_x, prev_y) = (x, y)
    debug_state = debug_state.previous

for row in debug_map:
    for c in row:
        if c in ['^', '>', 'v', '<']:
            print(colored(c, 'green'), end=' ')
        else:
            print(c, end=' ')
    print('\n')