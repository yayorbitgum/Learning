# Pull from openweathermap.org to display current weather forecasts.
# https://openweathermap.org/forecast5

# TODO: Automate grabbing API key.
# TODO: Automate grabbing city.list.json, and decompressing.
# TODO: Live display on website.
# ------------------------------------------------------------------------------
# Imports ----------------------------------------------------------------------
# ------------------------------------------------------------------------------
import os
import shutil
import sys

import requests
import json
# Speed up any repeated calls with Least Recently Used cache.
from functools import lru_cache
from bisect import bisect
from time import sleep
from datetime import datetime, timedelta
# Fuzzy input matching when API rejects user input.
from location_parser import fuzzy_find_city, city_list_filepath
# config is where your unique API key is stored as a string.
from config import my_key
import error_messages as errors
# For type-hinting.
from requests import Response
# rich module imports for making a colorful and stylized console-based UI.
# https://rich.readthedocs.io/en/latest/console.html
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich import box

# ------------------------------------------------------------------------------
# Variables --------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Data is only updated once every 10 minutes on their servers.
api_delay_in_sec = 600
animation_delay = 0.5
min_in_sec = 60
color_shift_amt = 120

accepted_code = 200
unauth_code = 401
not_found_code = 404

json_folder_path = 'json_files'
console = Console(color_system='truecolor')


# ------------------------------------------------------------------------------
# Classes ----------------------------------------------------------------------
# ------------------------------------------------------------------------------
class WeatherAPIData:
    """Object for examining and presenting weather data from API requests.
    forecast_index accepts int between 0 and 40. Each index is a 3 hour forecast
    interval. 0 index is live weather (I might be wrong on 0 being live)."""

    def __init__(self, weather_json, forecast_index: int):
        self.forecast_index = forecast_index
        self.weather = weather_json
        # JSON data.
        self.city_name   = self.weather['city']['name']
        self.id          = self.weather['city']['id']
        self.latitude    = self.weather['city']['coord']['lat']
        self.longitude   = self.weather['city']['coord']['lon']
        self.country     = self.weather['city']['country']
        self.population  = self.weather['city']['population']
        self.temperature = self.weather['list'][forecast_index]['main']['temp']
        self.feels_like  = self.weather['list'][forecast_index]['main']['feels_like']
        self.temp_min    = self.weather['list'][forecast_index]['main']['temp_min']
        self.temp_max    = self.weather['list'][forecast_index]['main']['temp_max']
        self.pressure    = self.weather['list'][forecast_index]['main']['pressure']
        self.humidity    = self.weather['list'][forecast_index]['main']['humidity']
        self.description = self.weather['list'][forecast_index]['weather'][0]['description']
        self.wind_speed  = self.weather['list'][forecast_index]['wind']['speed']
        self.wind_dir    = self.weather['list'][forecast_index]['wind']['deg']
        self.visibility  = self.weather['list'][forecast_index]['visibility']
        self.timestamp   = self.weather['list'][forecast_index]['dt_txt']
        self.data = {"ID": self.id,
                     "City name": self.city_name,
                     "Country": self.country,
                     "Latitude": self.latitude,
                     "Longitude": self.longitude,
                     "Population": self.population,
                     "Time block": self.timestamp,
                     "Weather description": self.description,
                     "Temperature": self.temperature,
                     "Minimum Temperature": self.temp_min,
                     "Maximum Temperature": self.temp_max,
                     "Feels like": self.feels_like,
                     "Pressure": self.pressure,
                     "Humidity": self.humidity,
                     "Wind Speed": self.wind_speed,
                     "Wind Direction": self.wind_dir,
                     "Visibility": self.visibility,
                     }
        # For our purposes, we'll always want fahrenheit so run update on init.
        self.update_k_to_f()
        # ----------------------------------------------------------------------

    def __iter__(self):
        return iter(self.data.items())

    # --------------------------------------------------------------------------
    def update_k_to_f(self):
        """
        This method runs the kelvin to farenheit conversion function
        on our temperature values.
        """
        self.temperature = round(convert_k_to_f(self.temperature))
        self.temp_min    = round(convert_k_to_f(self.temp_min))
        self.temp_max    = round(convert_k_to_f(self.temp_max))
        self.feels_like  = round(convert_k_to_f(self.feels_like))

    # --------------------------------------------------------------------------
    def show_all_data(self):
        """ Show all the data we got from requested weather forecast block."""
        table = Table()
        table.add_column('Description')
        table.add_column('Data')

        with Live(table, refresh_per_second=4):
            for description, data in self.data.items():
                table.add_row(description, str(data))

    # --------------------------------------------------------------------------
    def create_weather_panel(self) -> Panel:
        """
        Take in WeatherAPIData instances and chosen forecast index.
        Return rich Panel with weather info.
        """
        temp_colored = color_by_temperature(self.temperature)
        feels_colored = color_by_temperature(self.feels_like)
        wind_cardinal = wind_degrees_to_direction(self.wind_dir)
        lat = self.latitude
        lon = self.longitude

        panel_text = (f"{temp_colored} with {self.description.title()}\n"
                      f"Feels like {feels_colored}\n"
                      f"{wind_cardinal} @ [cyan]{self.wind_speed}mph[/]\n"
                      f"Humidity @ [cyan]{self.humidity}%[/]\n")

        # Forecast weather panel. ----------------------------------------------
        if self.forecast_index > 0:

            panel_text += f"{show_temp_difference(weather_now.temperature, self.temperature)}\n"
            panel = Panel(panel_text, box=box.ASCII)
            panel.title = f"[yellow]{self.forecast_index * 3} Hours[/]"
            return panel

        # Current weather panel. -----------------------------------------------
        elif self.forecast_index == 0:

            if self.population != 0:
                panel_text += f"\n[i]Population: {self.population:,}[/]"

            panel_text += f"[i]\nGPS: [link=https://www.google.com/maps/@{lat},{lon}]{lat}, {lon}[/link][/]"
            panel = Panel(panel_text, box=box.DOUBLE)
            state_code = determine_state_code(city_list_filepath, self.id)

            if state_code:
                panel.title = f"[yellow]{self.city_name}, {state_code}, {self.country}[/]"
            else:
                panel.title = f"[yellow]{self.city_name}, {self.country}[/]"

            return panel


# ------------------------------------------------------------------------------
# Functions --------------------------------------------------------------------
# ------------------------------------------------------------------------------
def request_weather_api(api_key: str, loc, api_city_id=None) -> (Response, str):
    """
    Request api from openweathermap.org.
    Return tuple of requests object, and specific city id if successful.
    https://openweathermap.org/current
    """
    # TODO:
    #  Most of the time we're making two API requests. Now that I've got
    #  fuzzy matching sped up fairly well, might as well always grab city id
    #  from fuzzy matching database first so we only ever make one.
    try:
        if api_city_id is not None:
            request = requests.get(f"http://api.openweathermap.org/data/2.5/forecast"
                                   f"?id={api_city_id}"
                                   f"&APPID={api_key}")
        else:
            request = requests.get(f"http://api.openweathermap.org/data/2.5/forecast"
                                   f"?q={loc}"
                                   f"&APPID={api_key}")

    except requests.exceptions.ConnectionError:
        console.print(f"[red]Connection failed! "
                      f"Check your internet connection and try again.[/]")
        initialize()
        return request_weather_api(api_key, loc)

    # API responses. -----------------------------------------------------------
    # 200 "OK".
    if request.status_code == accepted_code:
        request_and_id = [request, api_city_id]
        return request_and_id

    # 401 "Forbidden".
    elif request.status_code == unauth_code:
        console.print(errors.message_forbidden, style='red')
        initialize()
        return request_weather_api(key, loc)

    # 404 "Not Found".
    elif request.status_code == not_found_code:
        console.print('[red][i]Checking...[/][/]')
        # Openweathermap's API does not do partial matching, so it often rejects input.
        # So let's do our own fuzzy matching!
        choices = fuzzy_find_city(location)

        if len(choices) == 1:
            # Occurs when there's a perfect match for city and state based on input.
            city, state, api_city_id = choices[0].split(',')
            api_city_id = api_city_id.strip()
            # Now that we've got the exact city id, let's request API again.
            return request_weather_api(my_key, loc, api_city_id)

        elif len(choices) > 1:
            console.print('[red][i]Did you mean...[/][/]')
            for index, choice in enumerate(choices):
                console.print(f"{index}: {choice}")

            try:
                selection = int(input('Choose option number and hit enter (leave blank to cancel): '))
                location_string = choices[selection]

            except (IndexError, ValueError):
                initialize()
                return request_weather_api(key, loc)

            city, state, api_city_id = location_string.split(',')
            api_city_id = api_city_id.strip()
            # Now that we've got the exact city id, let's request API again.
            return request_weather_api(my_key, loc, api_city_id)

        # No choices were returned. Input was wildly misspelled.
        else:
            console.print("[red]Couldn't to find any matches! Try again.[/]")
            initialize()
            return request_weather_api(key, loc)

    # All other codes (will debug when I see them).
    else:
        console.print(f'[red]Response code {request.status_code}![/]')


# ------------------------------------------------------------------------------
def save_json(request, file_path: str):
    """Save the provided json file to given file_path."""
    if request is not None:
        with open(file_path, 'w') as file:
            json.dump(request.json(), file)


# json files are repeatedly opened to check weather API info as well as
# finding city ids for different searches. If we cache here, it cuts down
# time of subsequent searches significantly, at the cost of ~200mb memory usage.
@lru_cache
def open_json(file_path: str):
    """Open the json file in root folder. Return the json object."""
    try:
        with open(file_path, encoding='utf8') as file:
            json_data = json.load(file)
            return json_data
    except FileNotFoundError:
        print("Json file hasn't been created yet.")


def convert_k_to_f(k: int) -> float:
    """Convert kelvin to fahrenheit, return result."""
    celsius = k - 273.15
    fahrenheit = (celsius * 1.8) + 32
    return fahrenheit


def verify_key_exists(key_to_verify: str) -> str:
    """ Ensure user API key exists. If it does, return it."""
    if key_to_verify is not None:
        return key_to_verify
    else:
        raise errors.missing_api_exception


def shift_color(hex_value: hex, shift_amount: int) -> str:
    """Take a color hex value and add/subtract by given amount.
    Convert RBG hex value to RBG triplet value that rich can use.
    Return new color value."""
    # Hex values have a base of 16.
    hex_int = int(hex_value.lstrip('#'), 16)
    # Maximum color value is FFFFFF (255, 255, 255) RGB for non-HDR,
    # ie: 16,777,215 as int.
    if hex_int + shift_amount > 16777215:
        # Our way of looping back around.
        new_color = hex((hex_int + shift_amount) - 16777215).lstrip('0x')
    else:
        new_color = hex(hex_int + shift_amount).lstrip('0x')

    # We need the hex value to always be 6 digits to be a valid color.
    while len(new_color) < 6:
        new_color = '0' + new_color

    return f"#{new_color}"


def show_temp_difference(start_temp: int, end_temp: int) -> str:
    # Show temp difference between two temperatures, rounded. Return message string.
    temp_adjust = round(end_temp - start_temp, 1)
    if temp_adjust <= 0:
        return f"{temp_adjust}°F cooler."
    elif temp_adjust > 0:
        return f"{temp_adjust}°F warmer."


def color_by_temperature(temperature: int) -> str:
    """Take in temperature value and return text with color tags for use with rich ui."""
    # Color reference: https://rich.readthedocs.io/en/latest/_modules/rich/color.html
    temperature_breakpoints = (0, 32, 50, 65, 79, 89, 101, 115)
    temperature_colors = ("blue_violet",
                          "deep_sky_blue1",
                          "cyan",
                          "green",
                          "yellow",
                          "orange4",
                          "red",
                          "magenta",
                          "bright_magenta")
    bisect_index = bisect(temperature_breakpoints, temperature)
    color = temperature_colors[bisect_index]
    # Colors are assigned within strings like HTML tags, with [brackets][/brackets].
    return f"[{color}]{temperature}°F[/]"


def wind_degrees_to_direction(degrees: int) -> str:
    """Convert input degrees (int) to and return cardinal direction (str)."""
    breakpoints = (0, 15, 85, 95, 175, 185, 265, 275, 355, 360)
    directions = ("North", "North",
                  "Northeast", "East", "Southeast", "South",
                  "Southwest", "West", "Northwest", "North", "North")

    bisect_index = bisect(breakpoints, degrees)
    direction = directions[bisect_index]
    return direction


# Cached for multiple searches. This would ultimately create a bottleneck
# in create_ui() as far as not feeling snappy on load.
@lru_cache
def determine_state_code(city_list_file, weather_response_id) -> str:
    """
    Compare city IDs between city list and weather API data.
    Return state ID from match, or empty string if no match.
    """
    # Openweather API does not return state ID for whatever reason,
    # but it does return the city code, so we can use that to determine the state.
    state_code = ''
    location_data = open_json(city_list_file)
    for city in location_data:
        if weather_response_id == city['id']:
            state_code = city['state']
            return state_code

    return state_code


def create_ui(timestamp: datetime):
    """ Create our user interface within the console. Returns the rich Layout."""
    # https://rich.readthedocs.io/en/latest/index.html
    ui = Layout()
    ui.split_row(
        Layout(name='left'),
        Layout(name='right'),)

    panel_now = weather_now.create_weather_panel()
    panel_3h = weather_03h.create_weather_panel()
    panel_6h = weather_06h.create_weather_panel()
    panel_9h = weather_09h.create_weather_panel()
    panel_info = Panel(f"[i]{get_next_update_time(timestamp, api_delay_in_sec)}[/]")
    panel_info.box = box.ASCII
    panel_info.renderable += f"\n[i]Press [red]CTRL-C[/red] for different location at any time.[/]"

    # Future forecast panels.
    ui['right'].split_column(
        Layout(panel_3h, name='3h'),
        Layout(panel_6h, name='6h'),
        Layout(panel_9h, name='9h'),
    )

    # "now" and "info" panels.
    ui['left'].split_column(
        Layout(panel_now, name='now', ratio=3),
        Layout(panel_info, name='info'),
    )

    return ui


def get_next_update_time(start_time, delay_in_seconds):
    """Returns a string showing the next API update delay, and what time it will be."""
    next_time = start_time + timedelta(seconds=delay_in_seconds)
    next_up_minutes = round(delay_in_seconds / min_in_sec)
    next_up = next_time.strftime('%H:%M %p')

    hour, minute_and_period = next_up.split(':')
    if int(hour) > 12:
        hour = int(hour) - 12

    message = (f"Next update in [yellow]{next_up_minutes} minutes[/]"
               f" at [yellow]{hour}:{minute_and_period}[/].")

    return message


def clear_old_json():
    """Check for and delete old files from previous script runs generated in json_files."""
    json_file_list = [file for file in os.listdir('json_files') if file.endswith('json')]

    if json_file_list:
        console.print(f"[grey0][i] Deleting old files generated by {os.path.basename(__file__)}.[/][/]")

        for file in json_file_list:
            os.remove(os.path.join('json_files', file))
            console.print(f"[red][i]Removed {file} from 'json_files' folder.[/][/]")


def create_json_folder():
    try:
        os.mkdir(json_folder_path)
    except FileExistsError:
        pass


def get_user_input() -> str:
    """ Ask for user input for location, sanitizes input and returns titled string."""
    try:
        loc = input('Enter location: ')
    except EOFError:
        print("Exiting..")
        sys.exit()

    sanitized = "".join(char for char in loc if char.isalnum() or char == ',' or char == ' ')

    # If the user is cheeky and enters multiple commas, clear out excess.
    if sanitized.count(',') > 1:
        # (count - 1) means we leave one comma for (city, state) search in location_parser.
        sanitized = ''.join(sanitized.split(',', maxsplit=(sanitized.count(',') - 1)))

    return sanitized.title()


def set_json_path(loc) -> str:
    """Take in location and return file path for json based on loc name."""
    path = f'{json_folder_path}/{loc}.json'
    return path


def update_ui():
    current_time = datetime.now()
    interface = create_ui(current_time)
    return interface


# ------------------------------------------------------------------------------
def initialize():
    """
    Start up sequence: Create folder for api json, clear old json files,
    ask user for requested location, and set file path for json.
    Sets location and weather_path variables globally, thus
    can be called at any time to restart full sequence.
    """

    # TODO: Find a better way to do this. "location" is referenced directly in a
    # couple of separate functions. Might be confusing later on.
    global location
    global weather_path

    create_json_folder()
    clear_old_json()
    # Here's where the global variables are assigned.
    location = get_user_input()
    weather_path = f'{json_folder_path}/{location}.json'


# ------------------------------------------------------------------------------
# Start here.
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    initialize()
    key = verify_key_exists(my_key)
    response = request_weather_api(key, location)
    city_id = response[1]

    while True:
        # The one place (global) weather_path is referenced for now.
        save_json(response[0], weather_path)

        console.print('[grey0][i]Loading..[/][/]')
        weather_data = open_json(weather_path)
        weather_now = WeatherAPIData(weather_data, 0)
        weather_03h = WeatherAPIData(weather_data, 1)
        weather_06h = WeatherAPIData(weather_data, 2)
        weather_09h = WeatherAPIData(weather_data, 3)

        try:
            # This is how the UI is updated as you resize the window.
            with Live(update_ui(), refresh_per_second=4) as live:
                # We'll run this loop for 10 minutes because openweathermap API
                # only updates once every 10 minutes.
                for _ in range(api_delay_in_sec):
                    sleep(1)
                    live.update(update_ui())

        except KeyboardInterrupt:
            # So we can enter a different location at any time.
            initialize()
            response = request_weather_api(key, location)
            city_id = response[1]

        # Once the 10 minute delay timer expires, we request an updated forecast
        # and re-enter the while loop with the same location.
        response = request_weather_api(key, location, city_id)
