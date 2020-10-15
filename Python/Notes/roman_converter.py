# https://www.codewars.com/kata/51b6249c4612257ac0000005/python

numerals = ('I', 'V', 'X', 'L', 'C', 'D', 'M')
values = (1, 5, 10, 50, 100, 500, 1000)


def solution(roman: str):
    """
    Take in roman numeral string and output converted integer value.
    """
    roman_input = list(roman)
    conversion_output = 0
    axe_me = False

    for i, ch in enumerate(roman_input):
        index = numerals.index(ch)
        this_value = values[index]

        # If the current numeral has already been processed by last numeral,
        # then skip adding it and start next loop.
        if axe_me:
            axe_me = False
            continue

        try:
            next_numeral = roman_input[i+1]
            next_index = numerals.index(next_numeral)
            next_value = values[next_index]

        except IndexError:
            # If there is no next numeral, we're ready to just add and give result.
            conversion_output += this_value
            return conversion_output

        if next_value <= this_value:
            # If next numeral is lower then we know to just add the current one.
            conversion_output += this_value

        elif next_value > this_value:
            # If next numeral is larger, then we know we want to subtract them
            # together.
            result = next_value - this_value
            conversion_output += result
            # And to make sure to skip adding the next numeral since we just used it.
            axe_me = True

    return conversion_output


test_string = 'XIV'
print(solution(test_string))