day1_result = 0

class Hailstone:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

hailstones = []

with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        split_line = line.strip().split(' @ ')
        hailstones.append(Hailstone([int(c) for c in split_line[0].split(', ')], [int(c) for c in split_line[1].split(', ')]))

for i in range(len(hailstones) - 1):
    for j in range(i + 1, len(hailstones)):

        hailstone1 = hailstones[i]
        hailstone2 = hailstones[j]

        (x1, y1, z1) = (hailstone1.position[0], hailstone1.position[1], hailstone1.position[2])
        (vx1, vy1, vz1) = (hailstone1.velocity[0], hailstone1.velocity[1], hailstone1.velocity[2])
        # (x1, y1, z1) + t1 * (vx1, vy1, vz1)

        (x2, y2, z2) = (hailstone2.position[0], hailstone2.position[1], hailstone2.position[2])
        (vx2, vy2, vz2) = (hailstone2.velocity[0], hailstone2.velocity[1], hailstone2.velocity[2])
        # (x2, y2, z2) + t2 * (vx2, vy2, vz2)

        # ignore z-coordinates for now
        z1 = vz1 = z2 = vz2 = 0

        # consider equations
        # x1 + t1 * vx1 = x2 + t2 * vx2
        # y1 + t1 * vy1 = y2 + t2 * vy2

        # I assume no div by 0 until it happens, then fix it

        if (vx1 - vy1 * vx2 / vy2) == 0:
            # parallel in x and y
            continue

        t1 = (x2 - x1 + (y1 - y2) * vx2 / vy2) / (vx1 - vy1 * vx2 / vy2)

        x_by_1 = x1 + t1 * vx1
        y_by_1 = y1 + t1 * vy1

        t2 = (x_by_1 - x2) / vx2

        x_by_2 = x2 + t2 * vx2
        y_by_2 = y2 + t2 * vy2

        #print('t1:', t1,'x by 1:', x_by_1, 'y by 1:', y_by_1, sep=' ')
        #print('t2:', t2,'x by 2:', x_by_2, 'y by 2:', y_by_2, sep=' ')

        if t1 > 0 and t2 > 0 and 200000000000000 <= x_by_1 and x_by_1 <= 400000000000000 and 200000000000000 <= y_by_1 and y_by_1 <= 400000000000000:
            day1_result += 1
        
print('day 1 result: ', day1_result)