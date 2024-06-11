platform = []
tilted_platform = []
day1_result = 0

def print_platform(p) -> None:
    for row in p:
        print(''.join(row))

with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        platform.append(list(line.split()[0]))

platform.insert(0, ['#'] * len(platform[0]))

for i in range(len(platform)):
    tilted_platform.append([x for x in platform[i]])

    for j in range(len(platform[i])):
        if platform[i][j] == 'O':
            k = i
            if tilted_platform[i - 1][j] == '.':
                while tilted_platform[k - 1][j] == '.':
                    k -= 1

                tilted_platform[i][j] = '.'
                tilted_platform[k][j] = 'O'

            day1_result += len(platform) - k

print(day1_result)