import re
import math
import functools
import operator

def binomial(n, k) -> int:
    return functools.reduce(operator.mul, range(n, n - k, -1), 1) / math.factorial(k)

def binomialFormula(inputList, n) -> int:
    return sum([math.pow(-1, n - k + 1) * binomial(n - 1, k) * inputList[k] for k in range(n)])

numberPattern = re.compile("-?[0-9]+")
histories: [[int]] = []
part1Result = 0
part2Result = 0

with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        histories.append(list(map(lambda x: int(x), re.findall(numberPattern, line))))

for history in histories:
    for i in range(1, len(history), 1):
        if binomialFormula([history[k] for k in range(i)], i) == 0:
            # potentially found the zeroes row
            foundZeroRow = True

            for m in range(len(history) - i):
                if not binomialFormula([history[k + m] for k in range(i)], i) == 0:
                    foundZeroRow = False
                    break

            if foundZeroRow:
                prediction1 = - binomialFormula([history[len(history) - i + m + 1] for m in range(i - 1)] + [0], i)
                part1Result += prediction1
                
                prediction2 = math.pow(-1, i) * binomialFormula([0] + [history[m] for m in range(i - 1)], i)
                part2Result += prediction2
                break

print('result part 1: ', part1Result)
print('result part 2: ', part2Result)