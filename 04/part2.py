import re

sum = 0
numberPattern = re.compile('[0-9]+')
splitPattern = re.compile('[:|]')
matchesList = []

with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        split = re.split(splitPattern, line)
        winningNumberStrings = re.findall(numberPattern, split[1])
        ownNumberStrings = re.findall(numberPattern, split[2])

        winningNumbers = list(map(lambda x: int(x), winningNumberStrings))
        ownNumbers = list(map(lambda x: int(x), ownNumberStrings))

        winningNumbers.sort()
        ownNumbers.sort()

        matches = 0
        winningIndex = 0
        ownIndex = 0

        while winningIndex < len(winningNumbers) and ownIndex < len(ownNumbers):
            winningNumber = winningNumbers[winningIndex]
            ownNumber = ownNumbers[ownIndex]

            if winningNumber == ownNumber:
                matches += 1
            
            if winningNumber < ownNumber:
                winningIndex += 1
            else:
                ownIndex += 1

        matchesList.append(matches)

length = len(matchesList)
valueList = [0] * length
sum = 0

for i in range(length, 0, -1):
    cardValue = 1
    for j in range(matchesList[i - 1]):
        if i + j < length:
            cardValue += valueList[i + j]
    valueList[i - 1] = cardValue
    sum += cardValue

print(sum)