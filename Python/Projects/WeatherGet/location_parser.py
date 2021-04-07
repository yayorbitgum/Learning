# TODO:
#   For city.list.json, nest one additional dictionary depth based on each letter
#   of the alphabet, so that we first only search the matching starting letter
#   of our search term. Divide the entire list by 26 elements, rather than thousands.
#
# city.list.json is pulled from
# http://bulk.openweathermap.org/sample/city.list.json.gz

# Imports. ---------------------------------------------------------------------
import json
import sys
from fuzzywuzzy import fuzz
from rich.console import Console
from error_messages import missing_city_list
from collections import defaultdict
import string


# Variables. -------------------------------------------------------------------
city_list_filepath = 'city.list.json'
city_list_alphabet_filepath = 'city.list.alphabet.json'
console = Console(color_system='truecolor')


# Functions. -------------------------------------------------------------------
def read_city_json(file):
    """
    Read city file and return json object.
    Exits with helpful message if not found.
    """
    try:
        with open(file, encoding='utf8') as locations:
            json_data = json.load(locations)
            if json_data:
                return json_data
            else:
                console.print(missing_city_list)
                sys.exit()

    except FileNotFoundError:
        console.print(missing_city_list)
        sys.exit()


def alphabetizer():
    """
    Add alphabet as keys to city.list.json to partially speed up searching.
    """
    file_path = city_list_filepath
    new_path = city_list_alphabet_filepath
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


def verify_alphabet_nesting(path):
    """
    Make sure alphabetized json key length is 27 (26 letters + 1 special).
    Return True if so.
    """
    try:
        with open(path) as json_file:
            data = json.load(json_file)

            if len(data) == 27:
                return True
            else:
                return False

    except FileNotFoundError:
        return False


def fuzzy_find_city(loc=None) -> list:
    """
    Check locations list json for best matches of user input.
    Return list of best city 'name' and 'state' matches.
    """
    best_choices = []
    # TODO: Implement alphabetized search.
    locations = read_city_json(city_list_alphabet_filepath)
    if loc is None:
        user_input = input('Enter location (city, state): ')
    else:
        user_input = loc

    if ',' in user_input:
        city, state = user_input.split(',')
        city = city.strip().title()
        state = state.upper().strip()
    else:
        city = user_input.strip().title()
        state = None

    # --------------------------------------------------------------------------
    for letter in locations:
        if city.startswith(letter):

            for location in locations[letter]:
                ratio = fuzz.partial_ratio(location['name'], city)

                # Perfect match for city and state. ----------------------------
                if ratio == 100 and location['state'] == state:
                    console.print(f"[grey0]Perfect match: {location['name']}, {location['state']}[/]")
                    # If we found the exact city and state with 100% ratio,
                    # clear the list and return single value.
                    del best_choices
                    best_choices = [f"{ratio}%: "
                                    f"{location['name']}, "
                                    f"{location['state']}, "
                                    f"{location['id']}"]
                    return best_choices

                # 70%+ match for location, and exact match for state. ----------
                elif ratio >= 70 and location['state'] == state and state is not None:
                    console.print(f"[grey0]Possible match: {location['name']}, {location['state']}[/]")
                    best_choices.append(f"{ratio}%: "
                                        f"{location['name']}, "
                                        f"{location['state']}, "
                                        f"{location['id']}")

                # 80%+ match for location name only. ---------------------------
                elif ratio >= 80:
                    console.print(f"[grey0]Possible match: {location['name']}, {location['state']}[/]")
                    best_choices.append(f"{ratio}%: "
                                        f"{location['name']}, "
                                        f"{location['state']}, "
                                        f"{location['id']}")
    # --------------------------------------------------------------------------
    # For sorting by prefix numbers [match ratios] in string.
    best_choices.sort()
    best_choices.reverse()
    return best_choices


# ------------------------------------------------------------------------------
if __name__ == '__main__':

    alphabet_result = verify_alphabet_nesting(city_list_alphabet_filepath)
    if alphabet_result:
        print("Alphabetized json is proper length!")
    else:
        print("Alphabetizing city.list.json..")
        alphabetizer()
        print("Verifying..")
        if alphabet_result:
            print("Done!")
        else:
            print(f"Unexpected key length. Ensure city.list.json is populated.")

    results = fuzzy_find_city()
    for result in results:
        print(result)