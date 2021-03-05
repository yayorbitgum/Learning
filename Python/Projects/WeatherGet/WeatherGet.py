# Pull from openweathermap.org to current weather and the weather in the next 3 hours.
# https://openweathermap.org/forecast5


# Imports ----------------------------------------------------------------------
import requests
import json
# config is where you'll store your unique API key as a string.
# In this case, I store it as a string named "my_key" and import here.
from config import my_key
from time import sleep
from datetime import datetime, timedelta
# rich module imports for making a colorful and stylized console-based UI.
# https://rich.readthedocs.io/en/latest/console.html
from rich.console import Console

# Variables --------------------------------------------------------------------
# reference "city.list.json" provided by openweathermap.org.
# You can pass in coordinates and other parameters, but IDs are more precise.
# TODO: User input for location, then find closest (fuzzy) match in city.list.
city_id = 4544349
file_name = f'{city_id}_weather.json'
animation_delay = 0.5
min_in_sec = 60
accepted_response = 200
unauthorized_response = 401
# Data is only updated once every 10 minutes on their servers.
api_request_delay_in_seconds = 600
# Here's how we'll make everything pretty.
console = Console(color_system='truecolor')


# Functions --------------------------------------------------------------------
def save_json(res):
    """Save the json file to root folder."""
    with open(file_name, 'w') as file:
        json.dump(res.json(), file)
        print(f"Updated weather data in {file_name} successfully.")


def open_json():
    """Open the json file in root folder. Return the json object."""
    try:
        with open(file_name) as file:
            json_data = json.load(file)
            return json_data

    except FileNotFoundError:
        print("Json file hasn't been created yet.")


def k_to_f(k: int) -> float:
    """
    Converts kelvin to celsius, then to fahrenheit. Pass in kelvin first.
    Converting directly from K to F gave me differing temperature results.
    I don't understand why. Yet.
    """
    celsius = k - 273.15
    fahrenheit = (celsius * 1.8) + 32
    return fahrenheit


def verify_key_exists(key: str) -> str:
    # TODO: Help user automatically grab API key and save into their own config.py.
    """ Ensure user API key exists. If it does, return it."""
    if key is not None:
        return key
    else:
        raise Exception('You need an API key from openweathermap.org to grab current weather data.\n'
                        'Register, generate a key, and save that key as a string in config.py.\n'
                        'You can find your key(s) here --> https://home.openweathermap.org/api_keys')


def color_shift(hex_value: hex, shift_amount: int) -> str:
    """Take a color hex value and add/subtract by given amount.
    Convert RBG hex value to RBG triplet value that rich can use.
    Return new color value."""

    # Hex values have a base of 16.
    hex_int = int(hex_value.lstrip('#'), 16)

    # Max color value can only be FFFFFF.
    if hex_int + shift_amount > 16777215:
        new_color = '0000FF'
    else:
        new_color = hex(hex_int + shift_amount).lstrip('0x')
        # We need the hex value to always be 6 digits to be a valid color.
        while len(new_color) < 6:
            new_color = '0' + new_color

    return f"#{new_color}"


# ------------------------------------------------------------------------------
def main():
    """
    Main loop to make requests and dig through the json file to display
    weather data we want.
    """
    while True:
        validated_key = verify_key_exists(my_key)
        response = requests.get(f"http://api.openweathermap.org/data/2.5/forecast"
                                f"?id={city_id}"
                                f"&APPID={validated_key}")

        # (1/3) ----------------------------------------------------------------
        # Make sure we succeeded before we try to save it.
        if response.status_code == accepted_response:
            # Save the request so we don't have to pull from API over and over.
            save_json(response)
            weather = open_json()
            city_name = weather['city']['name']
            # ['list'][0] is current weather.
            # ['list'][1], or [2], etc would be forecast.
            # Each new list is 3 hours forecast ahead of last list. There are 40.

            # Current: [0]
            cur_description = weather['list'][0]['weather'][0]['description']
            cur_temps = weather['list'][0]['main']

            # 3 hours from now: [1]
            fut_description = weather['list'][1]['weather'][0]['description']
            fut_temps = weather['list'][1]['main']

            # Convert temps to F, then round up decimal points to 1.
            cur_temperature = round(k_to_f(cur_temps['temp']), 1)
            cur_feels_like = round(k_to_f(cur_temps['feels_like']), 1)
            fut_temperature = round(k_to_f(fut_temps['temp']), 1)

            cur_humidity = fut_temps['humidity']
            fut_humidity = fut_temps['humidity']

            # Makes forecast temp change easier to digest.
            temp_adjust = round(fut_temperature - cur_temperature, 1)
            if temp_adjust < 0:
                fut_temp_text = f"{temp_adjust}° cooler at {fut_temperature}° F."
            elif temp_adjust > 0:
                fut_temp_text = f"{temp_adjust}° warmer at {fut_temperature}° F."

            # ------------------------------------------------------------------
            # Lines into list to be animated.
            readout_lines = [f"--- {city_name} ---",
                             f"{cur_description.capitalize()}.",
                             f"{cur_humidity}% humidity.",
                             f"{cur_temperature}° F current temp.",
                             f"{cur_feels_like}° F feeling.\n",
                             f"---",
                             f"Coming up in 3 hours:\n",
                             f"{fut_description.capitalize()}.",
                             f"{fut_humidity}% humidity.",
                             f"{fut_temp_text}",
                             f"---\n"]

            # Console output animation loop.
            color = '#00FF00'
            for line in readout_lines:
                # TODO: Make better color gradient animations.
                color = color_shift(color, 120)
                console.print(line, justify="center", style=color)
                sleep(animation_delay)

            # ------------------------------------------------------------------
            time = datetime.now()
            update_delay_delta = timedelta(seconds=api_request_delay_in_seconds)
            next_update_time = time + update_delay_delta

            console.print(f"Next update in {round(api_request_delay_in_seconds / min_in_sec)} "
                          f"minutes at {next_update_time.strftime('%H:%M')}.\n\n")

        # (2/3) ----------------------------------------------------------------
        elif response.status_code == unauthorized_response:
            console.print("Your key was rejected with a 401 response code (Unauthorized).\n"
                          "Did you setup your API key properly?\n"
                          "Double check at --> https://openweathermap.org/api "
                          "for the 'Current Weather Data'. Click Subscribe and choose "
                          "the free option.\n"
                          "Then, check for your API key at --> https://home.openweathermap.org/api_keys\n"
                          "Enter that key in config.py and try again.", style='red')

        # (3/3) ----------------------------------------------------------------
        else:
            console.print(f"\n\n\nResponse code is {response.status_code}. \n\n\n", style='red')

        # ----------------------------------------------------------------------
        # Wait this long before querying again.
        sleep(api_request_delay_in_seconds)


# Program-----------------------------------------------------------------------
main()
