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
            new_dict['*'].append(city)
            break

# utf8 encoding and ensure_ascii=False required to account for cities like
# Ḩeşār-e Sefīd, Āzādshahr, and any other special characters across the globe.
with open(new_path, 'w', encoding='utf8') as output:
    json.dump(new_dict, output, sort_keys=True, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # If this script is run directly, we can do a quick test to see the new json breakdown.
    # This is helpful to see that we cut worst case scenario from
    # 209k down to 24k fuzzy matches at the slowest end.
    print(f"Dictionary length: {len(new_dict)}.")
    full_length = 0

    for key, value in new_dict.items():
        full_length += len(value)
        print(f"{key} contains {len(value):,} values.")

    print(f"\nTotal of {full_length:,} locations.")