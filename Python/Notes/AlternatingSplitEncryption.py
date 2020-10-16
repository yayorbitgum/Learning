# https://www.codewars.com/kata/57814d79a56c88e3e0000786/python
# My very bad but technically correct solution!
# In the future I should try to refactor this with better slicing and things.

def encrypt(text, n):
    # "If the input-string is null or empty return exactly this value!"
    # "If n is <= 0 then return the input text."
    if not text or text == '' or n <= 0:
        return text

    evens = ""
    odds = ""
    result = text

    for x in range(0, n):
        # Split evens and odds into temporary separate strings.
        # Apparently I could have done all the following with:
        # result = text[1::2] + text[::2]            Welp lol.
        for i, ch in enumerate(result):
            if i % 2 == 0:
                evens += ch
            else:
                odds += ch
        # Join the two halves together.
        result = odds + evens
        evens = ''
        odds = ''

    return result


def decrypt(encrypted_text, n):
    # "If the input-string is null or empty return exactly this value!"
    # "If n is <= 0 then return the input text."
    if not encrypted_text or encrypted_text == '' or n <= 0:
        return encrypted_text

    result = ""
    # This will initially be a float.
    half_length = len(encrypted_text)/2
    # Run this many times for our set encryption level.
    for x in range(0, n):
        # For our first run:
        if result == "":
            # If the amount of text is evenly cut in half:
            if half_length % 1 == 0:
                half_length = int(half_length)
                # Undo the joining of the two halves with slicing in the middle,
                # and temporarily store then in "first" and "second".
                first = encrypted_text[:half_length]
                second = encrypted_text[-half_length:]
            else:
                # Undo joining, and extend second half to grab last odd character.
                first = encrypted_text[:int(half_length)]
                second = encrypted_text[int(-half_length)-1:]

            count = 0
            # Rejoin them one character a time from each half.
            while len(first) > 0 or len(second) > 0:
                # Evens:
                if count % 2 == 0:
                    # Append character.
                    result += second[:1]
                    # Pop character out so we don't append it again.
                    second = second[1:]
                    count += 1
                # Odds:
                else:
                    result += first[:1]
                    first = first[1:]
                    count += 1

        # For subsequent runs:
        else:
            # Duplicate code here from above with slight changes.
            # Probably should make another function since this is smelly.
            if half_length % 1 == 0:
                half_length = int(half_length)
                # Undo the joining of the two halves by slicing the middle.
                first = result[:half_length]
                second = result[-half_length:]
            else:
                first = result[:int(half_length)]
                second = result[int(-half_length)-1:]
            # After we grab the halves, reset the result string so we don't
            # duplicate characters with these subsequent runs.
            result = ''
            count = 0
            # Rejoin them one character a time from each half.
            while len(first) > 0 or len(second) > 0:
                # Evens:
                if count % 2 == 0:
                    result += second[:1]
                    second = second[1:]
                    count += 1
                # Odds:
                else:
                    result += first[:1]
                    first = first[1:]
                    count += 1

    return result


# Testing. ---------------------------------------------------------------------
encrypt_me = 'Encrypt me daddy oh wow yes very nice okay!'
encryption_level = 100_000
encrypted = encrypt(encrypt_me, encryption_level)
decrypted = decrypt(encrypted, encryption_level)
print(f"input is    : {encrypt_me}")
print(f"encrypted is: {encrypted}")
print(f"decrypted is: {decrypted}")
