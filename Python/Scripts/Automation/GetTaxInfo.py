# Simple script to get amount of taxes owed/paid based on 2021 tax brackets.
# Honestly just wanted to see if I could do this programmatically.
# TODO: Get tax brackets automatically depending on the year, current and historical.
# TODO: Find reliable site to scrape for the above.
# ------------------------------------------------------------------------------
import sys
import shutil
import re

# ------------------------------------------------------------------------------
console_width, lines = shutil.get_terminal_size()
divisor = "-" * console_width
tax_brackets = ((0.1, 9_875),
                (0.12, 40_125),
                (0.22, 85_525),
                (0.24, 163_300),
                (0.32, 207_350),
                (0.35, 518_400),
                (0.37, 10_000_000_000))


# ------------------------------------------------------------------------------
def get_user_input() -> float:
    """Gets user input and returns annual income equivalent."""
    try:
        amt = input('Income: ')
        if ',' in amt:
            amt = amt.replace(',', '')
        amt = convert_to_annual(amt)
        return amt

    except ValueError:
        print("Please enter a number.")
        return get_user_input()


def convert_to_annual(amt: str) -> float:
    """Convert input based on weekly or monthly indicators. Return annual equivalent."""
    words = re.split('per|/| ', amt)
    monthly = ['month', 'mnth', 'mth', 'm']
    weekly = ['week', 'wk', 'w']
    amt = float(words[0])

    if "biweekly" in words:
        amt *= 24
        return amt

    for word in monthly:
        if word in words:
            amt *= 12
            return amt

    for word in weekly:
        if word in words:
            amt *= 48
            return amt

    return amt


def get_take_home(salary) -> float:
    """Get net income after taxes based on 2021 US tax brackets."""
    taxes = 0
    start = True
    # We don't need to run through the brackets if we make less than the upper limit
    # of the bottom tax bracket.
    if salary <= tax_brackets[0][1]:
        take_home = salary - (salary * tax_brackets[0][0])
        return take_home

    # We'll loop through each bracket to tax each bucket separately.
    for tax, bracket_upper in tax_brackets:
        if not start:
            if salary > bracket_upper:
                taxes += (bracket_upper - bracket_lower) * tax
            else:
                taxes += (salary - bracket_lower) * tax
                break

        bracket_lower = bracket_upper + 1
        start = False

    result = salary - taxes
    return result


def get_taxed_amt(salary, post_tax_amt) -> float:
    """ Return difference to show taxes paid."""
    return salary - post_tax_amt


def round_decimal(number) -> float:
    """Round to nearest penny, return rounded value."""
    return round(number, 2)


# ------------------------------------------------------------------------------
def main():
    income = round_decimal(get_user_input())
    take_home = round_decimal(get_take_home(income))
    monthly = round_decimal(take_home // 12)
    weekly = round_decimal(take_home // 48)
    taxed_amt = round_decimal(get_taxed_amt(income, take_home))

    print(f"\n{divisor}\n"
          f"Annual income earned: ${income:,}\n"
          f"Taxes owed/paid: ${taxed_amt:,}\n"
          f"Net income: ${take_home:,}\n"
          f"Monthly take-home: ${monthly:,}\n"
          f"Weekly: ${weekly:,}\n"
          f"{divisor}\n")


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"{divisor}\n"
          f"Enter annual income for 2021 to get tax bracket information.\n"
          f"Hit CTRL-C to quit at any time.\n"
          f"{divisor}\n")

    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Exiting.")
            sys.exit()