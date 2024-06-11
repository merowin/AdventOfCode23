def recursive(condition_record_part, groups) -> int:
    if len(groups) == 0:
        return 0 if '#' in condition_record_part else 1
    
    group = groups[0]
    isLast = (len(groups) == 1)
    restGroupLength = sum([groups[i] for i in range(1, len(groups))]) + (0 if isLast else len(groups) - 1)

    if (group + restGroupLength) > len(condition_record_part):
        # can't fit the groups at all
        return 0
    
    result = 0
    for i in range(1 + len(condition_record_part) - restGroupLength - group):
        if ('#' in condition_record_part[:i]) or ('.' in condition_record_part[i:i + group]) or (not isLast and condition_record_part[i + group] == '#'):
            # invalid group placement
            continue

        result += recursive(condition_record_part[i + group + (0 if isLast else 1):], groups[1:])

    return result

part1Result = 0
with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        split = line.split()
        condition_record, damaged_groups = split[0], list(map(lambda x: int(x), split[1].split(',')))
        possibilities = recursive(condition_record, damaged_groups)
        part1Result += possibilities

print('part 1 result: ', part1Result)