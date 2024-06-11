import re

map = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9, 
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
    }

sum = 0
pattern = re.compile("([0-9]|zero|one|two|three|four|five|six|seven|eight|nine)")
with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        length = len(line)-1
        firstMatch = re.search(pattern, line)
        index = firstMatch.start()
        match = None

        while (True):
            lastMatch = match
            match = re.search(pattern, line[index:length])
            if (match == None):
                break
            index += match.start() + 1
        
        first = map[firstMatch[0]]
        last = map[lastMatch[0]]
        sum += first * 10 + last
print(sum)