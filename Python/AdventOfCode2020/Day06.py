# https://adventofcode.com/2020/day/6

# There must be a blank line at the end of the input file, or the final group
# will be lost.
with open('inputs\day06_input.txt', 'r') as file:
    file = file.read()


# We'll split by each unique line so group break points (blank spaces) are still
# accounted for in this list.
data = file.split('\n')
print(data)


def count_answers():
    group_answers = []
    running_total = 0

    for answers in data:
        if len(answers) != 0:
            group_answers += [letter for letter in answers]

        # This is how we'll catch new lines (len of 0), ie a different group.
        else:
            # Remove duplicates.
            unique_answers = set(group_answers)
            running_total += len(unique_answers)
            # Reset for the next group of answers.
            group_answers.clear()

    # This would mean there's no blank line at the end of the input file.
    if group_answers:
        unique_answers = set(group_answers)
        running_total += len(unique_answers)
        group_answers.clear()

    return running_total


print(count_answers())