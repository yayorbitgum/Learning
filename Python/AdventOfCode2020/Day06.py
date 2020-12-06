# https://adventofcode.com/2020/day/6

with open('inputs\day06_input.txt', 'r') as file:
    file = file.read()


# We'll split by each unique line so group break points (blank spaces) are still
# accounted for in this list.
data = file.split('\n')


# ------------------------------------------------------------------------------
def count_answers_part_one():
    group_answers = []
    running_total = 0

    for answers in data:
        # This is how we'll catch new lines (len of 0), ie a different group.
        if len(answers) != 0:
            group_answers += [letter for letter in answers]
        else:
            # Remove duplicates.
            unique_answers = set(group_answers)
            running_total += len(unique_answers)
            # Reset for the next group of answers.
            group_answers.clear()

    # This would mean there's no blank line at the end of the input file.
    # In that case, this catches the last group that would be missed.
    if group_answers:
        unique_answers = set(group_answers)
        running_total += len(unique_answers)

    return running_total


# ------------------------------------------------------------------------------
def count_answers_part_two():
    group_answers = []
    running_total = 0
    person_count = 0
    # I'm keeping track of the current group for debugging purposes here.
    current_group = 1

    for answers in data:
        # This is how we'll catch new lines (len of 0), ie a different group.
        if len(answers) != 0:
            person_count += 1
            group_answers += [letter for letter in answers]
        else:
            # I was sorting here for easier debugging view.
            group_answers.sort()
            unique_answers = set(group_answers)
            for answer in unique_answers:
                if group_answers.count(answer) == person_count:
                    running_total += 1
            # Reset for the next group of answers.
            group_answers.clear()
            person_count = 0
            current_group += 1

    # This would mean there's no blank line at the end of the input file.
    # In that case, this catches the last group that would be missed.
    if group_answers:
        group_answers.sort()
        unique_answers = set(group_answers)
        for answer in unique_answers:
            if group_answers.count(answer) == person_count:
                running_total += 1

    return running_total


# ------------------------------------------------------------------------------
print(count_answers_part_one())
print(count_answers_part_two())
