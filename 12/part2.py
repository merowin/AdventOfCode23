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

    # only for debugging
    #results_data = []

    result = 0
    for i in range(len(groups) + 1):
        (left_record, left_groups) = record[:split_start], groups[:i]

        result_left = controller_function(left_record, left_groups)
        if result_left == 0:
            continue
        
        (right_record, right_groups) = record[split_end:], groups[i:]

        result_right = controller_function(right_record, right_groups)

        #results_data.append((right_record, right_groups, result_right, left_record, left_groups, result_left))

        result += result_left * result_right

    #print('************************')
    #print('splitter')
    #print('input:', record, groups, sep=' ')
    #for (right_record, right_groups, result_right, left_record, left_groups, result_left) in results_data:
    #    print('left:', left_record, left_groups, result_left, sep=' ')
    #    print('right:', right_record, right_groups, result_right, sep=' ')
    #
    #print('resulting in:', result, sep=' ')

    return result

# chooses one sequence of consecutive '#', assigns a group to it and splits the problem
def assigner_function(record, groups) -> int:
    result = 0
    (start, end) = find_central_match(record, damagedPattern)

    # for debugging
    #results_data = []

    for i, group in enumerate(groups):
        if group <= len(record) and group >= end - start:
            for pos_start in range(end - group, start + 1):
                if pos_start < 0 or pos_start + group > len(record):
                    continue

                if (pos_start > 0 and record[pos_start - 1] == '#') or (pos_start + group < len(record) and record[pos_start + group] == '#'):
                    continue

                record_left, groups_left = record[:max(0, pos_start - 1)], groups[:i]

                left_result = controller_function(record_left, groups_left)

                if left_result == 0:
                    continue

                record_right, groups_right = record[pos_start + group + 1:], groups[i + 1:]

                right_result = controller_function(record_right, groups_right)
                result += left_result * right_result

                #results_data.append((record_left, groups_left, left_result, record_right, groups_right, right_result))

    #print('************************')
    #print('assigner')
    #print('input:', record, groups, sep=' ')
    #for (left_record, left_groups, result_left, right_record, right_groups, result_right) in results_data:
    #    print('left:', left_record, left_groups, result_left, sep=' ')
    #    print('right:', right_record, right_groups, result_right, sep=' ')
    #
    #print('resulting in:', result, sep=' ')

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
        print(possibilities)
        part2Result += possibilities

print('part 2 result: ', part2Result)