class Brick:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.below = []

        self.init_coords()

    def init_coords(self):
        self.coordinate_vecs = []

        for x in range(self.start[0], self.end[0] + 1):
            for y in range(self.start[1], self.end[1] + 1):
                for z in range(self.start[2], self.end[2] + 1):
                    self.coordinate_vecs.append([x, y, z])

    # for debugging
    def __repr__(self):
        return repr(vars(self))

bricks = []

with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        split = line.strip().split('~')
        start = [int(c) for c in split[0].split(',')]
        end = [int(c) for c in split[1].split(',')]
        bricks.append(Brick(start, end))


min_x = min([brick.start[0] for brick in bricks] + [brick.end[0] for brick in bricks])
max_x = max([brick.start[0] for brick in bricks] + [brick.end[0] for brick in bricks])

min_y = min([brick.start[1] for brick in bricks] + [brick.end[1] for brick in bricks])
max_y = max([brick.start[1] for brick in bricks] + [brick.end[1] for brick in bricks])

min_z = 1
max_z = max([brick.start[2] for brick in bricks] + [brick.end[2] for brick in bricks])

room = []
for z in range(min_z, max_z + 1):
    plane = []
    room.append(plane)
    for y in range(min_y, max_y + 1):
        line = []
        plane.append(line)
        for x in range(min_x, max_x + 1):
            line.append(None)

for brick in bricks:
    for coordinate_vector in brick.coordinate_vecs:
        [x, y, z] = coordinate_vector

        room[z - min_z][y - min_y][x - min_x] = brick

bricks.sort(key=lambda brick: brick.start[2])

for brick in bricks:
    falling_down = True

    for coordinate_vector in brick.coordinate_vecs:
        [x, y, z] = coordinate_vector
        room[z - min_z][y - min_y][x - min_x] = None

    z_shift = 0
    while falling_down:

        for coordinate_vector in brick.coordinate_vecs:
            [x, y, z] = coordinate_vector

            # check if brick landed

            if z + z_shift == min_z:
                falling_down = False
                #print('brick landed on ground')
                break

            below = room[z + z_shift - 1 - min_z][y - min_y][x - min_x]
            if not below is None:
                falling_down = False
                #print('brick landed on brick')
                break
        
        if falling_down:
            z_shift -= 1

    #print('brick has landed after falling ', -z_shift, ' spaces')
            
    support = set()
    for coordinate_vector in brick.coordinate_vecs:
        coordinate_vector[2] += z_shift
        [x, y, z] = coordinate_vector
        room[z - min_z][y - min_y][x - min_x] = brick

        
        if z > min_z:
            below = room[z - 1 - min_z][y - min_y][x - min_x]
            if not (below is None or below == brick):
                support.add(below)

    for other_brick in support:
        brick.below.append(other_brick)

day1_result = 0

for brick in bricks:
    can_disintegrate = True

    for coordinate_vector in brick.coordinate_vecs:
        [x, y, z] = coordinate_vector

        above = room[z][y][x]
        if not (above is None or above == brick) and len(above.below) == 1:
            # above would fall if this is disintegrated
            can_disintegrate = False
            break

    if can_disintegrate:
        day1_result += 1

print('day 1 result: ', day1_result)

# day 2

day2_result = 0

for brick in bricks:
    would_fall_set = set()

    for coordinate_vector in brick.coordinate_vecs:
        [x, y, z] = coordinate_vector

        above = room[z][y][x]
        if not (above is None or above == brick) and len(above.below) == 1:
            # above would fall if this is disintegrated
            would_fall_set.add(above)

    for other_brick in bricks:
        if len(other_brick.below) > 0 and all(b in would_fall_set for b in other_brick.below):
            would_fall_set.add(other_brick)

    print(len(would_fall_set))
    day2_result += len(would_fall_set)

print('day 2 result: ', day2_result)