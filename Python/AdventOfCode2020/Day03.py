# https://adventofcode.com/2020/day/3#part1

step = 3

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
        line *= biome_expansion
        full_terrain.append(line)


def toboggan_trees(terrain, start=0, tree_count=0, segment=0):
    end = start + 3

    if segment > len(full_terrain) - 1:
        return tree_count

    for obstacle in terrain[segment][start:end]:
        if obstacle == '#':
            tree_count += 1
        segment += 1
        start = end
        return toboggan_trees(terrain, start, tree_count, segment)


print(toboggan_trees(full_terrain))