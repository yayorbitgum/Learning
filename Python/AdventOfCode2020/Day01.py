# Advent of Code Day 1.

def find_twenty_twenty():
    with open('M:\Coding Content\input.txt', 'r') as file:
        check_me = file.readlines()

        # This seems like a silly approach,
        # but it works so I'll just go with it lol.
        for num_a in check_me:
            # Trying to cut down on *some* unnecessary searching here.
            if int(num_a) < 2020:
                for num_b in check_me:
                    # Further limiting search.
                    if int(num_a) + int(num_b) < 2020:
                        for num_c in check_me:
                            a = int(num_a.strip())
                            b = int(num_b.strip())
                            c = int(num_c.strip())

                            if a + b + c == 2020:
                                return a * b * c


print(find_twenty_twenty())