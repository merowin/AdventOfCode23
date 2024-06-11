import re

sum = 0
lineCount = 0
redMax = 12
greenMax = 13
blueMax = 14

patternRed = re.compile('[0-9]+(?= red)')
patternGreen = re.compile('[0-9]+(?= green)')
patternBlue = re.compile('[0-9]+(?= blue)')

with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        lineCount += 1
        gamePossible = True

        for round in line.split(';'):
            redMatch  = re.search(patternRed, round)
            greenMatch  = re.search(patternGreen, round)
            blueMatch  = re.search(patternBlue, round)

            red = 0 if redMatch == None else int(redMatch[0])
            green = 0 if greenMatch == None else int(greenMatch[0])
            blue = 0 if blueMatch == None else int(blueMatch[0])
            
            if ((red > redMax) | (green > greenMax) | (blue > blueMax)):
                gamePossible = False
                break

        if (gamePossible):
            sum += lineCount

print(sum)