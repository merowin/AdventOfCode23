dig_plan = []

with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        split = line.strip().split(' ')
        dig_plan.append((split[0], int(split[1]), split[2]))

(x, y) = (0, 0)
(x_prev, y_prev) = (0, 0)
A = 1

for (d, a, c) in dig_plan:

    if d == 'U':
        y -= a
        A += a
    if d == 'R':
        x += a
        A += a
    if d == 'D':
        y += a
    if d == 'L':
        x -= a
    
    A += (x + x_prev) * (y - y_prev) / 2
    (x_prev, y_prev) = (x, y)

print(A)