def sum_galaxy_pair_dist(sorted_coordinates: [int], expansion: int) -> int:
    index_bound = len(sorted_coordinates)
    index = 0
    distance = 0
    empty_coordinate_number = 0
    last_coordinate = 0

    while index < index_bound:
        coordinate = sorted_coordinates[index]

        if last_coordinate < coordinate:
            empty_coordinate_number += coordinate - last_coordinate - 1
            last_coordinate = coordinate

        # second factor equals (index - (index_bound - (index + 1)))
        # this is the coefficient of the expanded coordinate in the whole sum
        distance += (coordinate + (empty_coordinate_number * expansion)) * (2 * index - index_bound + 1)
        index += 1

    return distance

galaxies_X: [int] = []
galaxies_Y: [int] = []

with open('input.txt', encoding="utf-8") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        line = lines[i]

        for j in range(len(line)):
            if line[j] == '#':
                galaxies_X.append(j)
                galaxies_Y.append(i)

galaxies_X.sort()
galaxies_Y.sort()

part1_distance_X = sum_galaxy_pair_dist(galaxies_X, 1)
part1_distance_Y = sum_galaxy_pair_dist(galaxies_Y, 1)

part2_distance_X = sum_galaxy_pair_dist(galaxies_X, 999999)
part2_distance_Y = sum_galaxy_pair_dist(galaxies_Y, 999999)

print('day 1 result: ', part1_distance_X + part1_distance_Y)
print('day 2 result: ', part2_distance_X + part2_distance_Y)