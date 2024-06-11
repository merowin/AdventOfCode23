import numpy as np

class Hailstone:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

hailstones = []

with open('C:\\Users\\Lenovo\\source\\repos\\AdventOfCode23\\24\\input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        split_line = line.strip().split(' @ ')
        hailstones.append(Hailstone(
            np.array([int(c) for c in split_line[0].split(', ')]),
            np.array([int(c) for c in split_line[1].split(', ')])))

min_x = min(x.position[0] for x in hailstones)
min_y = min(x.position[1] for x in hailstones)
min_z = min(x.position[2] for x in hailstones)
min_vector = np.array([min_x, min_y, min_z])

# shift all hailstones to reduce rounding errors
# will shift back at the end
for hailstone in hailstones:
    hailstone.position -= min_vector

search_treshold = 10000
epsilon = 10000

hailstone1 = hailstones[0]
hailstone2 = hailstones[1]

# consider possible times to hit first and second hailstones
for t1 in range(1, search_treshold):
    for t2 in range(1, search_treshold):

        if t1 == t2:
            continue

        if t1 == 5 & t2 == 4:
            pass

        # consider hitting hailstone 1 at time t1,
        # and hailstone 2 at time t2

        w1 = hailstone1.position + t1 * hailstone1.velocity
        w2 = hailstone2.position + t2 * hailstone2.velocity

        velocity = (w2 - w1) / (t2 - t1)
        start = w1 - t1 * velocity

        sx, sy, sz = start[0], start[1], start[2]
        vx, vy, vz = velocity[0], velocity[1], velocity[2]

        #test
        #if np.linalg.norm(start + t1 * velocity - w1) > 1:
        #    print('Warning 1')
        #if np.linalg.norm(start + t2 * velocity - w2) > 1:
        #    print('Warning 2')

        # test if this also hits other hailstones

        failed_test = False
        for other_hailstone in hailstones:
            if other_hailstone == hailstone1 or other_hailstone == hailstone2:
                continue

            other_start = other_hailstone.position
            other_velocity = other_hailstone.velocity

            o_sx, o_sy, o_sz = other_start[0], other_start[1], other_start[2]
            o_vx, o_vy, o_vz = other_velocity[0], other_velocity[1], other_velocity[2]

            if vx - vy * o_vx / o_vy == 0:
                #parallel in x / y
                failed_test = True
                break

            # t1 = (x2 - x1 + (y1 - y2) * vx2 / vy2) / (vx1 - vy1 * vx2 / vy2)
            time = (o_sx - sx + (sy - o_sy) * o_vx / o_vy) / (vx - vy * o_vx / o_vy)
            o_time = (sx + time * vx - o_sx) / o_vx

            #test
            #if abs((sx + time * vx) - (o_sx + o_time * o_vx)) > 10:
            #    print('warning, implementation error 1')
            #if abs((sy + time * vy) - (o_sy + o_time * o_vy)) > 10:
            #    print('warning, implementation error 2')

            # test if z-coordinates also equal at this time
            if abs(time - o_time) > 100 or abs((sz + time * vz) - (o_sz + o_time * o_vz)) > epsilon:
                failed_test = True
                break

        if not failed_test:
            print(start + min_vector)
            print(velocity)