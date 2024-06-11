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

position: CrossRoad = [x for x in crossRoads if x.label == "AAA"][0]
length = len(firstLine) - 1
count = 0

while position.label != "ZZZ":
    c = firstLine[count % length]
    count += 1

    if c == "L":
        position = position.left
    else:
        position = position.right

print(count)