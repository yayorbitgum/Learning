# https://www.codewars.com/kata/581e014b55f2c52bb00000f8/train/python
# To get the ASCII code of a character, use the ord() function.
# The opposite would be the chr() function.
# Swapped characters pretty easily with a, b = b, a
# Some simple regex.

import re


def decipher_this(string: str):
    words = string.split()
    # Spot our ascii codes (match numbers 0-9 that are 2-3 characters long)
    ascii_match = re.compile('([0-9]{2,3})')
    no_ascii = []
    deciphered = []

    # Use regex to convert ascii codes to letters.
    for word in words:
        im_ascii = ascii_match.search(word)
        ch_code = im_ascii.group(0)
        # Swap out ascii code with character.
        new_word = word.replace(ch_code, chr(int(ch_code)))
        no_ascii.append(new_word)

    # Swap second and last letters.
    for word in no_ascii:
        if len(word) > 1:
            chs = list(word)
            # This is so cool that you can even do it like this. Thanks Python.
            chs[1], chs[-1] = chs[-1], chs[1]
            word = ''.join(chs)
            deciphered.append(word)
        else:
            deciphered.append(word)
            continue

    return ' '.join(deciphered)


test1 = '65 119esi 111dl 111lw 108dvei 105n 97n 111ka'
test2 = '84eh 109ero 104e 115wa 116eh 108sse 104e 115eokp'
test3 = '84eh 108sse 104e 115eokp 116eh 109ero 104e 104dare'

print(decipher_this(test1))