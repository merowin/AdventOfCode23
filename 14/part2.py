platform = []
number_of_cycles = 1000000000
#number_of_cycles = 1
day2_result = 0
platform_history = []

def print_platform(p) -> None:
    for row in p:
        print(''.join(row))

def copy_platform(p) -> any:
    return [[char for char in row] for row in p]

def areEqualPlatforms(p1, p2) -> bool:
    return all(all(p1[i][j] == p2[i][j] for j in range(len(p1[i]))) for i in range(len(p1)))

with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        platform.append(list(line.split()[0]))

platform.insert(0, ['#'] * len(platform[0]))
platform.append(['#'] * len(platform[0]))
for row in platform:
    row.insert(0, '#')
    row.append('#')

tilted_platform = copy_platform(platform)

cycle = 1
stop_criterium = None
cycle_length = None
while cycle <= number_of_cycles and (stop_criterium == None or not ((cycle - 1) % cycle_length == stop_criterium)):

    # north
    for i in range(len(tilted_platform)):

        for j in range(len(tilted_platform[i])):
            if tilted_platform[i][j] == 'O':
                k = i
                if tilted_platform[i - 1][j] == '.':
                    while tilted_platform[k - 1][j] == '.':
                        k -= 1

                    tilted_platform[i][j] = '.'
                    tilted_platform[k][j] = 'O'

    #west
    for i in range(len(tilted_platform)):
        for j in range(len(tilted_platform[i])):

            if tilted_platform[i][j] == 'O':
                k = j
                if tilted_platform[i][j - 1] == '.':
                    while tilted_platform[i][k - 1] == '.':
                        k -= 1

                    tilted_platform[i][j] = '.'
                    tilted_platform[i][k] = 'O'

    #south
    for i in range(len(tilted_platform) - 1, -1, -1):
        for j in range(len(tilted_platform[i])):

            if tilted_platform[i][j] == 'O':
                k = i
                if tilted_platform[i + 1][j] == '.':
                    while tilted_platform[k + 1][j] == '.':
                        k += 1

                    tilted_platform[i][j] = '.'
                    tilted_platform[k][j] = 'O'

    #east
    for i in range(len(tilted_platform)):
        for j in range(len(tilted_platform[i]) - 1, -1, -1):

            if tilted_platform[i][j] == 'O':
                k = j
                if tilted_platform[i][j + 1] == '.':
                    while tilted_platform[i][k + 1] == '.':
                        k += 1

                    tilted_platform[i][j] = '.'
                    tilted_platform[i][k] = 'O'
    
    if (stop_criterium is None) and cycle > 3 and areEqualPlatforms(tilted_platform, platform_history[cycle // 2]):
        cycle_length = cycle - (cycle // 2) - 1
        print(cycle_length)
        stop_criterium = number_of_cycles % cycle_length
        print(stop_criterium)

    platform_history.append(copy_platform(tilted_platform))

    cycle += 1

print_platform(tilted_platform)

for i in range(len(tilted_platform)):
    for c in tilted_platform[i]:
        if c == 'O':
            day2_result += len(tilted_platform) - i - 1

print(day2_result)
# cycle length of 7