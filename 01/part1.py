import re

sum = 0
with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        numbers = re.findall("[0-9]", line)
        first = int(numbers[0])
        last = int(numbers[len(numbers)-1])
        sum += first * 10 + last

print(sum)