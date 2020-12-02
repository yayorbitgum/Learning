# Advent of Code Day 2.
import re


# Part 1!
with open('M:\Coding Content\input2.txt', 'r') as file:
    regex = re.compile('(\d+)-(\d+)\s(\w):\s(\w+)')
    valid_count = 0

    for line in file:
        for group in regex.findall(line):
            lower = int(group[0])
            upper = int(group[1])
            letter = group[2]
            # The full password to check.
            check_me = group[3]
            if lower <= check_me.count(letter) <= upper:
                valid_count += 1

    print(valid_count)


# Part 2!
with open('M:\Coding Content\input2.txt', 'r') as file:
    regex = re.compile('(\d+)-(\d+)\s(\w):\s(\w+)')
    valid_count = 0

    for line in file:
        rules = line.strip()
        for group in regex.findall(rules):
            index_a = int(group[0])-1
            index_b = int(group[1])-1
            letter = group[2]
            # The full password to check.
            check_me = group[3]
            first = check_me[index_a]
            second = check_me[index_b]

            if first == letter and second != letter:
                valid_count += 1
            elif second == letter and first != letter:
                valid_count += 1

    print(valid_count)