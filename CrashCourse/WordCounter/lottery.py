# ///////////////////// External Modules /////////////////////////
from random import randint
from sys import exit as stop_program


# ///////////////////// Classes / Methods /////////////////////////
# Problems 9-14, 9-15 from Crash Course book, but I wanted to go a lot of steps further and actually
#   randomly generate the winning numbers too.

class Play:
    """
    This class simulates playing the lottery.
    We enter our picks, and simulate drawings.
    But we simulate a lot of them very quickly..
    As fast as possible, until we finally win.
    """

    def __init__(self):
        self.winning_numbers = []
        # Powerball unused for now.
        self.powerball = 0

        self.my_numbers = []
        self.my_powerball = 7    # unused for now.

    def get_user_numbers(self):
        print(f"It's time to play the fuckin lottery.\n"
              f"Choose 5 numbers, one at a time.\n")
        # Reset my numbers on input, for new pick, so we avoid problems.
        self.my_numbers = []
        count = 0

        # Now we can loop 5 times for new picks.
        while True:
            if count < 5:
                # Take input
                current_number = int(input(f"\n#{count+1} of 5: Enter a number between 1 and 59: "))

                if current_number in range(1, 59):
                    count += 1
                    # Add to list
                    self.my_numbers.append(current_number)

                else:
                    print("Yea what the hell was that entry? Try again.\n")
                    self.get_user_numbers()

            elif count == 5:
                print(f"\nOkay! Your picks are: {self.my_numbers}")
                print("To win, you have to match all 5 numbers. "
                      "If you can't, it fails and draws new numbers again and again, until you do win."
                      "\n Are you ready?")
                input("Press enter to start.")
                self.odds_of_win()

    def generate_drawing(self):
        # Reset list if new drawing:
        self.winning_numbers = []
        # Draw 5 times for regular drawing with loop
        for slot in range(0, 5):
            # Add a random number between 1 and 59 to the list
            self.winning_numbers.append(randint(1, 59))

        # Draw once for powerball.
        self.powerball = randint(1, 29)

    def display_initial_numbers(self):
        print(f"The winning numbers are as follows! \n")

        for index, number in enumerate(self.winning_numbers):
            counter = index+1
            print(f"Drawing {counter} of {len(self.winning_numbers)}: {number}")
        print(f"And the powerball is {self.powerball}! \n")

    def odds_of_win(self):
        print(f"Your numbers are: {self.my_numbers} and {self.my_powerball}")
        print(f"The winning numbers are: {self.winning_numbers} and {self.powerball}")
        failure_count = 0
        win_count = 0
        close_calls = 0

        # Trying to think of a loop to see how many attempts it takes to win.
        while True:
            for number in self.my_numbers:
                # If we found all 5 numbers 5 times in a row, then we won.
                if win_count >= 5:
                    print(f"Wow you finally won. It only took {failure_count:,} attempts to do it.")
                    print(f"Just to confirm, your numbers were {self.my_numbers}.")
                    print(f"And the final winning numbers were {self.winning_numbers}.")

                    # And restart if we want to.
                    choice = input(f"\nWanna play again? y/n \n")
                    if choice == 'n':
                        stop_program()
                    else:
                        self.get_user_numbers()

                else:
                    # If we find your current number in winning list, add +1 to count
                    if number in self.winning_numbers:
                        # We add one to win count.
                        win_count += 1
                        # But only print it if we match 4 or more in a row, to reduce spam.
                        if win_count == 4:
                            close_calls += 1
                            print(f"Fuck. You've had {close_calls} close calls "
                                  f"out of {failure_count:,} attempts.")

                        elif win_count == 5:
                            print("You matched all 5 in a row!!")

                    else:
                        # As soon as a number fails, we lose, so reset everything,
                        # generate new winning numbers, and add one to fail count.
                        win_count = 0
                        failure_count += 1
                        self.generate_drawing()
                        # This is so it only prints a failure update every million fails, to reduce log spam.
                        # If current count divided by 1,000,000 = no remainder, then print that count.
                        if failure_count % 1_000_000 == 0:
                            print(f"Failure count: {failure_count:,}.")


# ///////////////////// Program /////////////////////////
# Instantiate.
PlayLottery = Play()
# Do stuff.
PlayLottery.generate_drawing()
PlayLottery.get_user_numbers()