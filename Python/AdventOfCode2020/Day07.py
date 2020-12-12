# https://adventofcode.com/2020/day/7
# My WIP solution to Day 7. I'll have to come back to this some other day lol.
# I need to learn how breadth first searches work.
# I may be making this harder on myself by parsing as nested dictionaries, but
# I'm not quite sure yet.
import re

# ------------------------------------------------------------------------------
with open('inputs\day07_input.txt', 'r') as file:
    file = file.read()

all_bag_input = re.split('contain|\n', file)


# ------------------------------------------------------------------------------
def build_master_bag_dict(bag_info) -> dict:
    """Take in bag_info input file (list of bags split by 'contain' and new lines).
       Build a bag master dictionary and its nested dictionaries for bag values.
       Return the bag master dictionary."""
    bag_master_dict = {}
    bag_kv_regex = re.compile('(\d) (.*)')

    for bag_line in bag_info:
        bag = bag_line.strip().rstrip('.')
        # Based on our input, this will only ever happen if key_bag has been defined.
        if bag == "no other bags":
            bag_master_dict[key_bag] = bag
        # Indicates key bag, contains 3 words every time.
        elif len(bag.split()) == 3:
            key_bag = bag
            bag_master_dict[bag] = {}
        # Otherwise it's an internal bag with associated counts.
        else:
            internal_bags_list = bag.split(',')
            internal_bags = {}

            for item in internal_bags_list:
                for group in bag_kv_regex.findall(item):
                    bag_count = group[0]
                    bag_type = group[1]
                    # need to change every occurrence of "bag" to "bags" so
                    # values can also be nested keys for recursive searching.
                    if bag_type.endswith('g'):
                        bag_type += 's'
                    internal_bags[bag_type] = bag_count

            bag_master_dict[key_bag] = internal_bags

    return bag_master_dict


def count_bags(bag, child_bag=None):
    # Loop through the internal bags.
    nested = big_bag_dictionary[bag]

    if bag != child_bag:
        print(f"Checking root: {bag}. Contains | {nested}")

    if 'shiny gold bags' in nested:
        print(f"{bag} contain a shiny gold bag! {nested}")
        checked_bags.append(bag)
        return 1

    if nested != 'no other bags':
        for bags in nested:
            if bags not in empty_bags:
                # If this current bag has no other bags inside of it, we need to skip it.
                if big_bag_dictionary[bags] == 'no other bags':
                    print(f"{bags} is empty.")
                    empty_bags.append(bags)
                    continue
                else:
                    if bags not in gold_bags:
                        print(f"---> Checking child bag {bags}")
                        checked_bags.append(bags)
                        return count_bags(bags, bags)
    else:
        empty_bags.append(nested)


# ------------------------------------------------------------------------------
big_bag_dictionary = build_master_bag_dict(all_bag_input)

empty_bags = []
gold_bags = []
checked_bags = []


# Loop through the base bags, during which we'll check nested bags with count_bags().
# I CAN'T FIGURE THIS OUT!! ARGHH
def double_check(count=0):
    for key in big_bag_dictionary:
        if key not in checked_bags:
            result = count_bags(key)
            if result is not None:
                count += result

    return count


print(double_check())