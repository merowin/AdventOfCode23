import re
from termcolor import colored
import os
os.system('color')

class Pipe:
    def __init__(self, symbol, x, y) -> None:
        self.symbol = symbol
        self.x = x
        self.y = y
        self.visited = False
        self.distanceFromStart = None
        (self.connectsUp, self.connectsRight, self.connectsDown, self.connectsLeft) = self.determineConnections()
        self.neighbours = []
        self.path = []
        self.onCycle = False
        self.inside = False

    def determineConnections(self) -> (bool, bool, bool, bool):
        if self.symbol == 'S':
            return (True, True, True, True)

        connectsUp = False
        connectsRight = False
        connectsDown = False
        connectsLeft = False

        if self.symbol == '|':
            connectsUp = True
            connectsDown = True

        if self.symbol == '-':
            connectsLeft = True
            connectsRight = True
                
        if self.symbol == 'L':
            connectsUp = True
            connectsRight = True

        if self.symbol == 'J':
            connectsUp = True
            connectsLeft = True

        if self.symbol == '7':
            connectsLeft = True
            connectsDown = True

        if self.symbol == 'F':
            connectsRight = True
            connectsDown = True

        return (connectsUp, connectsRight, connectsDown, connectsLeft)

    def connectTo(self, other) -> None:
        if self.neighbours.count(other) == 0:
            self.neighbours.append(other)

        if other.neighbours.count(self) == 0:
            other.neighbours.append(self)

# read input

pipeMap: [[Pipe]] = []

with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        pipeMap.append([Pipe(line[i], i, len(pipeMap)) for i in range(len(line) - 1)])

# connect pipes

y_max = len(pipeMap) - 1
start = None

for row in pipeMap:
    for pipe in row:
        x = pipe.x
        y = pipe.y

        if pipe.connectsUp and y > 0:
            otherPipe = pipeMap[y - 1][x]
            if otherPipe.connectsDown:
                pipe.connectTo(otherPipe)

        if pipe.connectsRight and x < len(row) - 1:
            otherPipe = row[x + 1]
            if otherPipe.connectsLeft:
                pipe.connectTo(otherPipe)

        if pipe.connectsDown and y < y_max:
            otherPipe = pipeMap[y + 1][x]
            if otherPipe.connectsUp:
                pipe.connectTo(otherPipe)

        if pipe.connectsLeft and x > 0:
            otherPipe = row[x - 1]
            if otherPipe.connectsRight:
                pipe.connectTo(otherPipe)

        if pipe.symbol == 'S':
            start = pipe

# find cycle with breadth first search
#
# note that this is overkill, since the pipes form a one-way connection
# i had initially interpreted the pipe connections differently, and then too lazy to simplify it

part1result = 0
queue = [([], 0, None, start)]

while len(queue) > 0:
    (path, distance, previousPipe, pipe) = queue.pop()

    if pipe.visited:
        part1result = distance
        for cyclePipe in path + pipe.path:
            cyclePipe.onCycle = True
        break
    
    pipe.visited = True
    pipe.distance = distance
    pipe.path = path

    queue = [(path + [pipe], distance + 1, pipe, neighbour) for neighbour in pipe.neighbours if not neighbour == previousPipe] + queue

# determine inside by detecting crossings

part2result = 0

for row in pipeMap:
    lastCycleEntry = None
    inside = False

    for pipe in row:

        if pipe.onCycle:
            if lastCycleEntry is None:
                if pipe.symbol == '|':
                    inside = not inside
                else:
                    lastCycleEntry = pipe.symbol
            else:
                crossing = (lastCycleEntry == 'L' and pipe.symbol == '7') or (lastCycleEntry == 'F' and pipe.symbol == 'J')
                if crossing:
                    inside = not inside
                
                if not pipe.symbol == '-':
                    lastCycleEntry = None
                
        elif inside:
                part2result += 1
                pipe.inside = True

#for row in pipeMap:
#    for pipe in row:
#        print(colored(pipe.symbol, ('red' if pipe.onCycle else ('blue' if pipe.inside else 'white'))), end='')
#    
#    print('\n')
                
print('part 1 result ', part1result)
print('part 2 result ', part2result)