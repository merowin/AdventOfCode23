import re

def adjacentMatches(starMatch: re.Match[str], numberMatch: re.Match[str]) -> bool:
    return (starMatch.start() <= numberMatch.end() and starMatch.start() >= numberMatch.start() - 1)

sum = 0
numberPattern = re.compile('[0-9]+')
starPattern = re.compile('[*]')

with open('input.txt', encoding="utf-8") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        line = lines[i]

        for starMatch in re.finditer(starPattern, line):
            adjacentNumbers = 0
            product = 1

            for numberMatch in re.finditer(numberPattern, line):
                if adjacentMatches(starMatch, numberMatch):
                    adjacentNumbers += 1
                    product *= int(numberMatch[0])
            
            if (i > 0):
                previousLine = lines[i - 1]

                for numberMatch in re.finditer(numberPattern, previousLine):
                    if adjacentMatches(starMatch, numberMatch):
                        adjacentNumbers += 1
                        product *= int(numberMatch[0])

            if (i < len(lines) - 1):
                nextLine = lines[i + 1]

                for numberMatch in re.finditer(numberPattern, nextLine):
                    if adjacentMatches(starMatch, numberMatch):
                        adjacentNumbers += 1
                        product *= int(numberMatch[0])

            print('------------')
            print(adjacentNumbers)
            if (starMatch.start() > 0 and starMatch.end() < len(line) - 1 and i > 0 and i < len(lines) - 1):
                print(lines[i - 1][starMatch.start() - 1:starMatch.end() + 1])
                print(lines[i][starMatch.start() - 1:starMatch.end() + 1])
                print(lines[i + 1][starMatch.start() - 1:starMatch.end() + 1])
            if adjacentNumbers == 2:
                sum += product

print(sum)