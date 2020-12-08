# https://adventofcode.com/2020/day/7
# My WIP solution to Day 7..
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
                    internal_bags[bag_type] = bag_count

            bag_master_dict[key_bag] = internal_bags

    return bag_master_dict


# ------------------------------------------------------------------------------
big_bag_dictionary = build_master_bag_dict(all_bag_input)


# TODO: How many bag colors can eventually contain at least one shiny gold bag?
count = 0
# Loop through the base bags.
for key in big_bag_dictionary:
    print(f"{key} -->")

    # Loop through the internal bags.
    items = big_bag_dictionary[key]
    try:
        for key_item in items:
            print(f"{items[key_item]} {key_item}")

    # We'll reach here if "no other bags" is the only value for this key.
    except TypeError:
        print(f"{items}")