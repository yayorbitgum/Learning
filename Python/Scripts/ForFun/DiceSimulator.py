# ///////////////////// External Modules /////////////////////////
from random import randint


# ///////////////////// Classes / Methods /////////////////////////
# Problem 9-13 in Crash Course, plus a lot of extra functionality I added to see if it would work.
class Die:
    def __init__(self, sides=6):
        self.sides = sides
        self.rolls = []
        self.die_amt = 0
        self.casts = 0

    def roll_die(self):
        # Do a roll for each dice we have.
        for die in range(0, self.die_amt):
            # And for each dice, throw it this many times.
            for cast in range(0, self.casts):
                # Now here's the dice rolling onto a random side.
                roll = randint(1, self.sides)
                # Add it to the list of our rolls.
                self.rolls.append(roll)

        print(f"Your rolls are as follows: \n")
        # enumerate so I can get the current index too, just for nice count format.
        for index, roll in enumerate(self.rolls):
            # Have to add 1 since index starts at zero. Otherwise it would start with "Roll 0:"
            count = index+1
            print(f"Roll {count}: {roll}")

    # All input needs to be converted to integers, since we'll be doing
    # some math (ie "range" above) with our input
    def input_dice_count(self):
        self.die_amt = int(input("How many dice are we rolling?\n"))

    def input_sides(self):
        self.sides = int(input("How many sides do your dice have?\n"))

    def input_max_cast(self):
        self.casts = int(input("How many times do we toss the dice?\n"))


# ///////////////////// Program /////////////////////////

# Create new instance of Die.
Play = Die()

# Call input methods so we know what to play with.
Play.input_dice_count()
Play.input_sides()
Play.input_max_cast()

# Roll that shit and see results.
Play.roll_die()

