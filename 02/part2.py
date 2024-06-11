import re

sum = 0
lineCount = 0

patternRed = re.compile('[0-9]+(?= red)')
patternGreen = re.compile('[0-9]+(?= green)')
patternBlue = re.compile('[0-9]+(?= blue)')

with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        redMax = 0
        greenMax = 0
        blueMax = 0

        for round in line.split(';'):
            redMatch  = re.search(patternRed, round)
            greenMatch  = re.search(patternGreen, round)
            blueMatch  = re.search(patternBlue, round)

            red = 0 if redMatch == None else int(redMatch[0])
            green = 0 if greenMatch == None else int(greenMatch[0])
            blue = 0 if blueMatch == None else int(blueMatch[0])
            
            if (red > redMax):
                redMax = red

            if (green > greenMax):
                greenMax = green

            if (blue > blueMax):
                blueMax = blue

        sum += redMax * greenMax * blueMax

print(sum)