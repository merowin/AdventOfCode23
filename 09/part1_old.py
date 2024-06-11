import re
import numpy as np
import numpy.polynomial.polynomial as polynomial

numberPattern = re.compile("-?[0-9]+")
histories: [[int]] = []
ep = 0.001
resultSum = 0

with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        histories.append(list(map(lambda x: int(x), re.findall(numberPattern, line))))

for history in histories:
    #print('******************')
    #print(histories.index(history))
    fittingDegree: int = None
    ableToFit = False

    #for degree in range(len(history)):
    degree = len(history) - 1
    p,[residuals, rank, singular_values, rcond] = polynomial.Polynomial.fit(x=range(len(history)), y=history, deg=degree, full=True)
    #pRound = list(map(lambda x: np.round(x), p))

    #values = polynomial.polyval(list(range(len(history))), p)
    #error = 0
    #for i in range(len(history)):
    #    error += abs(values[i] - history[i])
    #error = sum([abs(values[i] - history[i]) for i in range(len(history))])
    #print('error:', error)

    fits = True #error < ep
    
    if fits:
        resultSum += np.round(p(len(history)))
        ableToFit = True
        break

    if not ableToFit:
        print('warn')
    
print(resultSum)
'''
    extendedHistory = []
    not_found = True
    index = 0
    degree = None

    while not_found and index < len(history) - 1:
        index += 1

        extendedHistory.append([])
        for i in range(index):
            if i == 0:
                extendedHistory[i].append(history[-index] - history[-index - 1])
            else:
                extendedHistory[i].append(extendedHistory[i - 1][-1] - extendedHistory[i - 1][-2])

            print(extendedHistory[i])
            if len(extendedHistory[i]) > 2 and extendedHistory[i][0] == 0 and extendedHistory[i][1] == 0 and extendedHistory[i][2] == 0:
                not_found = False
                degree = index
                print(degree)
                break
                '''