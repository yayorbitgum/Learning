# This script formats city.list.json so that dictionaries are nested by keys
# for each letter of the alphabet (A-Z, with a 27th key '*' for special characters).
# This speeds up fuzzy matching significantly.
#
# Worst case fuzzy search was ~209k items before, down to ~24k after organizing.
#
# Since openweathermap API does not do partial matching (AFAIK), this script then
# takes user input, fuzzy matches (closest matches) within the city.list.alphabet.json
# file, and returns precise info (such as exact city database ID) that
# the openweathermap API will accept, so we can get accurate weather data back
# without needing to be exact with user input.
# We can also have the user confirm their intended location search this way. IE:
# "Did you mean Oklahoma City, OK or Oklahoma, OK" when searching for oklahoma.
#
# city.list.json is pulled from
# http://bulk.openweathermap.org/sample/city.list.json.gz
#
# Running this script directly will allow you to test fuzzy matching results,
# verify the json format is optimized for this searching, and if not, optimize it.
#
# TODO: Download city.list.json automatically.
# TODO: Or, better yet, make this into a website where the backend can update by itself.

# Imports. ---------------------------------------------------------------------
import json
import sys
from fuzzywuzzy import fuzz
from rich.console import Console
from error_messages import missing_city_list
from collections import defaultdict
from functools import lru_cache
import string

# Variables. -------------------------------------------------------------------
city_list_filepath = 'city.list.json'
city_list_alphabet_filepath = 'city.list.alphabet.json'
console = Console(color_system='truecolor')
ratio_partial_minimum = 80
ratio_full_minimum = 70
ratio_best_match = 100


# Functions. -------------------------------------------------------------------
@lru_cache
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
    Add alphabet as keys to city.list.json to significantly speed up fuzzy searching.
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
                new_dict['*'].append(city)
                break

    # utf8 encoding and ensure_ascii=False required for cities like
    # Ḩeşār-e Sefīd, Āzādshahr, and any other special characters across the globe.
    with open(new_path, 'w', encoding='utf8') as output:
        json.dump(new_dict, output, sort_keys=True, indent=4, ensure_ascii=False)


def verify_alphabet_nesting(path):
    """
    Make sure alphabetized json key length is 27 (26 letters + 1 special).
    Return True if so.
    """
    try:
        with open(path, encoding='utf8') as json_file:
            data = json.load(json_file)

            if len(data) == 27:
                return True
            else:
                return False

    except FileNotFoundError:
        return False


@lru_cache
def fuzz_ratio(city_input, territory_input, loc_city, loc_territory, loc_id):
    choices = set()
    ratio = fuzz.token_set_ratio(loc_city, city_input)

    # Perfect match for city and state.
    if ratio == ratio_best_match and loc_territory == territory_input:
        # If we found the exact city and state with 100% ratio,
        # we know we don't need anything else found before this result.
        del choices
        choices = {f"{ratio}%: "
                   f"{loc_city}, "
                   f"{loc_territory}, "
                   f"{loc_id}"}
        return choices

    # Match for location, and exact match for state.
    elif ratio >= ratio_full_minimum and loc_territory == territory_input and territory_input is not None:
        choices.add(f"{ratio}%: "
                    f"{loc_city}, "
                    f"{loc_territory}, "
                    f"{loc_id}")

    # Match for location name only.
    elif ratio >= ratio_partial_minimum:
        choices.add(f"{ratio}%: "
                    f"{loc_city}, "
                    f"{loc_territory}, "
                    f"{loc_id}")

    return choices


def fuzzy_find_city(loc=None) -> list:
    """
    Check locations list json for best matches of user input.
    Return list of best city 'name' and 'state' matches, with "none of the above"
    as the last option.
    """
    choices = set()
    locations = read_city_json(city_list_alphabet_filepath)
    if loc is None:
        # Loc should only be none if we're running location_parser directly.
        user_input = input('\nEnter location: ')
    else:
        user_input = loc

    if ',' in user_input:
        input_split = user_input.split(',')
        city = input_split[0].strip().title()
        # Territory could account for state or country.
        territory = input_split[-1].upper().strip()
    else:
        city = user_input.strip().title()
        territory = None

    # --------------------------------------------------------------------------
    for letter in locations:
        # City starts with english letter A to Z.
        if city.startswith(letter):
            for location in locations[letter]:
                # Perfect match means we don't need to search anymore.
                if location['name'] == city and location['state'] == territory:
                    return [f"{location['name']}, {location['state']}, {location['id']}"]
                else:
                    choices.update(
                        fuzz_ratio(
                            city,
                            territory,
                            location['name'],
                            location['state'],
                            location['id']
                        )
                    )
    # --------------------------------------------------------------------------
    # City name input doesn't start with any letter from english alphabet.
    # This means we're looking up weather on a foreign territory for sure.
    # Foreign territories will contain country name rather than state name.
    if not choices:
        for location in locations['*']:
            choices.update(
                fuzz_ratio(
                    city,
                    territory,
                    location['name'],
                    location['country'],
                    location['id']
                )
            )
    # --------------------------------------------------------------------------
    # We used a set initially to prevent duplicate results from fuzzy matching.
    # Now we convert to list so we can sort the choices based on most likely match
    # to least likely match.
    sorted_choices = list(choices)
    sorted_choices.sort()
    sorted_choices.append("None of the above.")
    return sorted_choices


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    console.print(f"\n[i]Running this script directly allows you to test fuzzy matching.[/]")
    console.print(f"[i]Acceptable minimal match is {ratio_partial_minimum}%, "
                  f"or {ratio_full_minimum}% if both city and state/territory match.[/]")
    alphabet_result = verify_alphabet_nesting(city_list_alphabet_filepath)

    if not alphabet_result:
        console.print("[red]Alphabetizing city.list.json..[/]")
        alphabetizer()
        print("Verifying..")
        if alphabet_result:
            print("Done!")
        else:
            print(f"Unexpected key length. Ensure city.list.json is populated.")

    while True:
        results = fuzzy_find_city()
        if results:
            for result in results:
                print(result)
        else:
            console.print(
                '[grey0]No viable matches (likeliness of match was too low to display).'
                '\nYou can lower the minimum ratio, but it will likely flood results '
                'with poor matches.[/]')
