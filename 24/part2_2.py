import time
import numpy as np

start = time.time()

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

#min_x = min(x.position[0] for x in hailstones)
#min_y = min(x.position[1] for x in hailstones)
#min_z = min(x.position[2] for x in hailstones)
#min_vector = np.array([min_x, min_y, min_z])

# shift all hailstones to reduce rounding errors
# will shift back at the end
#for hailstone in hailstones:
#    hailstone.position -= min_vector


# positions

s1x, s1y, s1z = _s1 = hailstones[0].position
S1 = np.array(_s1)

s2x, s2y, s2z = _s2 = hailstones[1].position
S2 = np.array(_s2)

s3x, s3y, s3z = _s3 = hailstones[2].position
S3 = np.array(_s3)


# velocities

v1x, v1y, v1z = _v1 = hailstones[0].velocity
V1 = np.array(_v1)

v2x, v2y, v2z = _v2 = hailstones[1].velocity
V2 = np.array(_v2)

v3x, v3y, v3z = _v3 = hailstones[2].velocity
V3 = np.array(_v3)


# right-side

b1 = np.cross(S2, V2) - np.cross(S1, V1)
b2 = np.cross(S2, V2) - np.cross(S3, V3)

b = np.concatenate([b1, b2])

# coefficients for Z x V
def cross_product_coefficients(Z):
    return [
        [0, -Z[2], Z[1]], # coefficients in x coordinate
        [Z[2], 0, -Z[0]], # coefficients in y coordinate
        [-Z[1], Z[0], 0]  # coefficients in z coordinate
        ]



cross1_sx, cross1_sy, cross1_sz = cross_product_coefficients(S2 - S1)
cross1_vx, cross1_vy, cross1_vz = cross_product_coefficients(V2 - V1)

a1x = np.array(cross1_sx + cross1_vx)
a1y = np.array(cross1_sy + cross1_vy)
a1z = np.array(cross1_sz + cross1_vz)



cross2_sx, cross2_sy, cross2_sz = cross_product_coefficients(S2 - S3)
cross2_vx, cross2_vy, cross2_vz = cross_product_coefficients(V2 - V3)

a2x = np.array(cross2_sx + cross2_vx)
a2y = np.array(cross2_sy + cross2_vy)
a2z = np.array(cross2_sz + cross2_vz)


A = np.array([a1x, a1y, a1z, a2x, a2y, a2z])

#print(np.linalg.cond(A))

#print('A: ')
#for row in A:
#    print(row)
#print('b: ', b)

L = np.linalg.solve(A, b)

#print('L: ', L)

#print('diff: ')
#diff = np.matmul(A, L) - b
#for row in diff:
#    print(row)

vx, vy, vz, sx, sy, sz = L

print(sx + sy + sz)

print(time.time() - start)