# city.list.json is pulled from
# http://bulk.openweathermap.org/sample/city.list.json.gz
import json
import sys
from fuzzywuzzy import fuzz
from rich.console import Console
from error_messages import missing_city_list

city_list_filepath = 'city.list.json'
console = Console(color_system='truecolor')


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


def fuzzy_find_city(loc=None) -> list:
    """
    Check locations list json (city.list.json) for best matches of user input.
    Return list of best city 'name' and 'state' matches.
    """
    best_choices = []
    locations = read_city_json(city_list_filepath)
    if loc is None:
        user_input = input('Enter location (city, state): ')
    else:
        user_input = loc

    if ',' in user_input:
        city, state = user_input.split(',')
        city = city.strip()
        state = state.upper().strip()
    else:
        city = user_input
        state = None

    # --------------------------------------------------------------------------
    for location in locations:
        ratio = fuzz.partial_ratio(location, city)

        # Perfect match for city and state. ------------------------------------
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

        # 70%+ match for location, and exact match for state. ------------------
        elif ratio >= 70 and location['state'] == state and state is not None:
            console.print(f"[grey0]Possible match: {location['name']}, {location['state']}[/]")
            best_choices.append(f"{ratio}%: "
                                f"{location['name']}, "
                                f"{location['state']}, "
                                f"{location['id']}")

        # 85%+ match for location name only. -----------------------------------
        elif ratio >= 85:
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
    results = fuzzy_find_city()
    for result in results:
        print(result)