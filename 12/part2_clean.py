import re
import math
import functools
import operator

operationalPattern = re.compile("[.]+")
damagedPattern = re.compile("[#]+")

dictionary = {}

def find_central_match(s, pattern) -> (int, int):
    length = len(s)
    middle = length // 2
    current_best = None
    dist = None
    index = 0

    while index < length:
        match = re.search(pattern, s[index:])
        if match is None:
            break

        (a, b) = match.span()
        (start, end) = (a + index, b + index)

        match_dist = min(abs(start - middle), abs(end - middle))

        if current_best == None or dist > match_dist:
            current_best = (start, end)
            dist = match_dist
        
        index = end

    return current_best

def binomial(n, k) -> int:
    return functools.reduce(operator.mul, range(n, n - k, -1), 1) / math.factorial(k)

# checks if dictionary contains a saved result for this
# calls the correct function for the job
def controller_function(record, groups) -> int:
    key = record + ''.join(str(x) + ',' for x in groups)
    savedResult = dictionary.get(key)

    if not savedResult == None:
        return savedResult

    if '.' in record:
        result = splitter_function(record, groups)
        dictionary[key] = result
        return result
    
    if '#' in record:
        result = assigner_function(record, groups)
        dictionary[key] = result
        return result
    
    result = multiplier_function(record, groups)
    dictionary[key] = result
    return result

# splits at one sequence of '...'
def splitter_function(record, groups) -> int:
    (split_start, split_end) = find_central_match(record, operationalPattern)

    result = 0
    for i in range(len(groups) + 1):

        result_left = controller_function(record[:split_start], groups[:i])
        if result_left == 0:
            continue

        result += result_left * controller_function(record[split_end:], groups[i:])

    return result

# chooses one sequence of consecutive '#', assigns a group to it and splits the problem
def assigner_function(record, groups) -> int:
    result = 0
    (start, end) = find_central_match(record, damagedPattern)

    for i, group in enumerate(groups):
        if group <= len(record) and group >= end - start:
            for pos_start in range(end - group, start + 1):
                if pos_start < 0 or pos_start + group > len(record):
                    continue

                if (pos_start > 0 and record[pos_start - 1] == '#') or (pos_start + group < len(record) and record[pos_start + group] == '#'):
                    continue

                left_result = controller_function(record[:max(0, pos_start - 1)], groups[:i])

                if left_result == 0:
                    continue

                result += left_result * controller_function(record[pos_start + group + 1:], groups[i + 1:])

    return result

# should only get called with consecutive '???...'
def multiplier_function(record, groups) -> int:
    free_space = len(record) - minRequiredSpace(groups)
    if free_space < 0:
        return 0
    
    groups_of_free_space = len(groups) + 1
    return binomial(free_space + groups_of_free_space - 1, groups_of_free_space - 1)

def minRequiredSpace(groups) -> int:
    length = len(groups)

    if length == 0:
        return 0
    
    return sum(groups) + length - 1

part2Result = 0
with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        split = line.split()
        base_record, base_groups = split[0], list(map(lambda x: int(x), split[1].split(',')))
        unfold_record = (base_record + '?') * 4 + base_record
        unfold_groups = base_groups * 5
        possibilities = controller_function(unfold_record, unfold_groups)
        part2Result += possibilities

print('part 2 result: ', part2Result)