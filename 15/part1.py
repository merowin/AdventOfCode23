def HASH(s: str) -> int:
    curr = 0
    for c in s:
        curr += ord(c)
        curr *= 17
        curr = curr % 256

    return curr

day1_result = 0

with open('input.txt', encoding="utf-8") as f:
    seq = f.readline().strip().split(',')
    for s in seq:
        day1_result += HASH(s)

print('day 1 result ', day1_result)