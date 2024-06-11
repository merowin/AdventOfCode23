import re

sum = 0
numberPattern = re.compile('[0-9]+')
symbolPattern = re.compile('[^(0-9.)]')

with open('input.txt', encoding="utf-8") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        line = lines[i]

        for numberMatch in re.finditer(numberPattern, line):
            foundSymbol = False
            startIndex = numberMatch.span()[0]
            endIndex = numberMatch.span()[1]
            
            if startIndex > 0 and line[startIndex - 1] != '.':
                foundSymbol = True
            
            if endIndex < len(line) - 1 and line[endIndex] != '.':
                foundSymbol = True
            
            if (i > 0):
                previousLine = lines[i - 1]

                for symbolMatch in re.finditer(symbolPattern, previousLine):
                    if symbolMatch[0] != '\n' and symbolMatch.start() >= startIndex - 1 and symbolMatch.start() <= endIndex:
                        foundSymbol = True

            if (i < len(lines) - 1):
                nextLine = lines[i + 1]

                for symbolMatch in re.finditer(symbolPattern, nextLine):
                    if symbolMatch[0] != '\n' and symbolMatch.start() >= startIndex - 1 and symbolMatch.start() <= endIndex:
                        foundSymbol = True

            if foundSymbol:
                sum += int(numberMatch[0])

print(sum)