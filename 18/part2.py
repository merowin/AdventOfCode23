dig_plan = []

with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        split = line.strip().split(' ')
        amount = int(split[2][2:-2], 16)
        d = split[2][-2]
        dig_plan.append((d, amount))

(x, y) = (0, 0)
(x_prev, y_prev) = (0, 0)
coords = []
A = 1

for (d, a) in dig_plan:

    if d == '3':
        y -= a
        A += a
    if d == '0':
        x += a
        A += a
    if d == '1':
        y += a
    if d == '2':
        x -= a
    
    coords.append((x, y))
    
    A += (x + x_prev) * (y - y_prev) / 2
    (x_prev, y_prev) = (x, y)

print(A)

