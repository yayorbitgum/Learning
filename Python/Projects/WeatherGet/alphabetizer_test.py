# Sped up fuzzy searching considerably by rebuilding the json for alphabetical search
# of city/location name first.
# This functionality was moved into location_parser.py

from collections import defaultdict
from location_parser import read_city_json
import string
import json

file_path = "city.list.json"
new_path = "city.list.alphabet.json"
city_file = read_city_json(file_path)
alphabet = string.ascii_uppercase
new_dict = defaultdict(list)


for city in city_file:
    count = 0
    for letter in alphabet:
        count += 1
        if city['name'].upper().startswith(letter):
            new_dict[letter].append(city)
            # Once we find the letter, break this loop or it'll copy this city 26 times.
            break

        elif count == 26:
            # We reach here if we've found a city that starts with a special character.
            new_dict['SPECIAL'].append(city)
            break

with open(new_path, 'w') as output:
    json.dump(new_dict, output, sort_keys=True, indent=4)


if __name__ == "__main__":

    print(f"Dictionary length: {len(new_dict)}.")
    for key, value in new_dict.items():
        print(f"{key} contains {len(value):,} values.")