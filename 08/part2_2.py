cycleLengths = [12643, 14257, 15871, 18023, 19637, 16409]

def euclid(a, b) -> int:
    c = max(a, b)
    d = min(a,b)

    while d != 0:
        c, d = d, c % d

    return c

def lcm(a, b) -> int:
    return (a * b) / euclid(a, b)

m = 1

for cycle in cycleLengths:
    m = lcm(m, cycle)

print(m)