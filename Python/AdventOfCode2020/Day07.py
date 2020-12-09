# https://adventofcode.com/2020/day/7
# My WIP solution to Day 7..
import re
from pprint import pprint

# ------------------------------------------------------------------------------
with open('inputs\day07_test.txt', 'r') as file:
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


def count_bags(bag, gold_count=0):
    # Loop through the internal bags.

    nested = big_bag_dictionary[bag]

    if 'shiny gold bags' in nested:
        print(f"{key} contain a shiny gold bag! {nested}")
        gold_count += 1

    if nested == 'no other bags':
        # TODO
        # Need to figure out how to return to parent dictionary.
        # Probably need some form of a queue.
        pass
    for bag in nested:
        return count_bags(bag, gold_count)

    return gold_count


# ------------------------------------------------------------------------------
big_bag_dictionary = build_master_bag_dict(all_bag_input)

# Loop through the base bags.
count = 0
for key in big_bag_dictionary:
    count += count_bags(key)

print(count)