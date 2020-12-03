# https://adventofcode.com/2020/day/3#part1
# https://adventofcode.com/2020/day/3#part2
import math

# ------------------------------------------------------------------------------
step = 3    # This only works for part one. For part 2 it's not long enough.
slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
results = []

# ------------------------------------------------------------------------------
with open('M:\Coding Content\day03_input.txt', 'r') as file:
    file_lines = file.readlines()
    line_count = len(file_lines)
    full_terrain = []

    # "...due to something you read about once involving arboreal genetics and
    # biome stability, the same pattern repeats to the right many times."
    # I don't know if this is exact, but it's long enough.
    biome_expansion = line_count // (len(file_lines[0]) // step)

    for line in file_lines:
        line = line.strip()
        line *= biome_expansion * 10    # "10" is a hamfisted fix for part 2, for now lol.
        full_terrain.append(line)


# ------------------------------------------------------------------------------
def toboggan_trees(terrain, slope: tuple, start=0, tree_count=0, segment=0):
    end = start + slope[0]

    if segment > len(terrain) - 1:
        return tree_count

    for obstacle in terrain[segment][start:end]:
        if obstacle == '#':
            tree_count += 1
        segment += slope[1]
        start = end
        return toboggan_trees(terrain, slope, start, tree_count, segment)


# ------------------------------------------------------------------------------
for slope in slopes:
    results.append(toboggan_trees(full_terrain, slope))

print(math.prod(results))