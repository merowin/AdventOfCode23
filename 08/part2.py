import re

class CrossRoad:
    def __init__(self, label, leftLabel, rightLabel) -> None:
        self.label = label
        self.leftLabel = leftLabel
        self.rightLabel = rightLabel
        self.left = None
        self.right = None

    def print(self) -> None:
        print(self.label, self.leftLabel, self.rightLabel, sep=", ")

crossRoads: [CrossRoad] = []
labelPattern = re.compile("[A-Z]{3}")
startNodes: [CrossRoad] = []

with open('input.txt', encoding="utf-8") as f:
    firstLine = f.readline()

    for line in f.readlines():
        labels = re.findall(labelPattern, line)
        if len(labels) > 0:
            crossRoads.append(CrossRoad(labels[0], labels[1], labels[2]))

for crossRoad in crossRoads:
    leftCandidates = [x for x in crossRoads if x.label == crossRoad.leftLabel]
    rightCandidates = [x for x in crossRoads if x.label == crossRoad.rightLabel]

    if len(leftCandidates) > 0:
        crossRoad.left = leftCandidates[0]

    if len(rightCandidates) > 0:
        crossRoad.right = rightCandidates[0]

    if crossRoad.label[2] == "A":
        startNodes.append(crossRoad)

# last character in line is \n
length = len(firstLine) - 1

for startNode in startNodes:
    position = startNode
    count = 0
    lastVisit = None

    print('*******************')
    print(startNode.label)
    print('*******************')

    while count < length * 1000:
        c = firstLine[count % length]
        count += 1

        if c == "L":
            position = position.left
        else:
            position = position.right

        if position.label[2] == "Z":
            print(count, end=' ')
            if not lastVisit is None:
                print('diff: ', count - lastVisit, end='')
            print("\r")
            lastVisit = count

