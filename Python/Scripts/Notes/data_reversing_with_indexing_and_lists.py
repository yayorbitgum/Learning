# https://www.codewars.com/kata/569d488d61b812a0f7000015/train/python
# A stream of data is received and needs to be reversed.
# Each segment is 8 bits long, meaning the order of these segments needs to be
# reversed.
# The total number of bits will always be a multiple of 8.
import random


def data_reverse(data):
    # A stream of data is received and reversed.
    # "The total number of bits will always be a multiple of 8."
    if len(data) % 8 == 0:
        # Get amount of segments (bytes, for this kata) so we can make
        # a for loop that covers any amount.
        segment_count = len(data)//8
        byte_lists = []

        for x in range(segment_count):
            # We'll make incrementing indexes so we can do any amount of loops.
            if x == 0:
                start = x
            else:
                # "end" won't be referenced before assignment because we'll
                # only reach this by having run the loop at least once.
                start = end

            end = start + 8
            data_byte = data[start:end]
            byte_lists.append(data_byte)

        byte_lists.reverse()
        # https://stackoverflow.com/a/952952/13627106
        # The kata needs the result to be one list of bits, so we'll unpack it.
        flattened_list = [item for sublist in byte_lists for item in sublist]
        return flattened_list

    else:
        print(f"Incomplete byte at end? Leftover is {len(data) % 8}.")


# Testing data sets. List generators for some so I don't have to write it all.
data1 = [1, 2, 3, 4, 5, 6, 7, 8, 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 10, 20, 30, 40, 50, 60, 70, 80]
data2 = [random.choice(range(0, 2)) for _ in range(64)]
data3 = [random.choice(range(0, 2)) for _ in range(80)]
data4 = [random.choice(range(0, 2)) for _ in range(800)]
data5 = [random.choice(range(0, 2)) for _ in range(960)]
inputs = [data1, data2, data3, data4, data5]

for i, d in enumerate(inputs):
    print(f"data{i+1}:")
    print(data_reverse(d))