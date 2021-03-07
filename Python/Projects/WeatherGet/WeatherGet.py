# Pull from openweathermap.org to display current weather forecasts.
# https://openweathermap.org/forecast5

# ------------------------------------------------------------------------------
# Imports ----------------------------------------------------------------------
# ------------------------------------------------------------------------------
import requests
import json
# config is where your unique API key is stored as a string.
from config import my_key
# Lengthy but helpful messages.
import error_messages as errors
from time import sleep
from datetime import datetime, timedelta
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
from rich.text import Text

# ------------------------------------------------------------------------------
# Variables --------------------------------------------------------------------
# ------------------------------------------------------------------------------
# reference "city.list.json" provided by openweathermap.org.
# You can pass in coordinates and other parameters, but IDs are more precise.
# TODO: User input for location, then find closest (fuzzy) match in city.list.
city_id = 4544349
file_name = f'{city_id}_weather.json'
animation_delay = 0.5
min_in_sec = 60
color_shift_amt = 120
accepted_response = 200
unauthorized_response = 401
# Data is only updated once every 10 minutes on their servers.
api_request_delay_in_seconds = 600
# Here's how we'll make everything pretty.
console = Console(color_system='truecolor')


# ------------------------------------------------------------------------------
# Classes ----------------------------------------------------------------------
# ------------------------------------------------------------------------------
class WeatherAPIData:
    """Object for examining and presenting weather data from api request.
    forecast_index accepts int between 0 and 40. Each index is a 3 hour forecast
    interval. 0 index is live weather."""

    def __init__(self, weather_json, forecast_index: int):
        self.weather = weather_json
        # JSON data.
        self.city_name   = self.weather['city']['name']
        self.temp        = self.weather['list'][forecast_index]['main']['temp']
        self.feels_like  = self.weather['list'][forecast_index]['main']['feels_like']
        self.temp_min    = self.weather['list'][forecast_index]['main']['temp_min']
        self.temp_max    = self.weather['list'][forecast_index]['main']['temp_max']
        self.pressure    = self.weather['list'][forecast_index]['main']['pressure']
        self.humidity    = self.weather['list'][forecast_index]['main']['humidity']
        self.description = self.weather['list'][forecast_index]['weather'][0]['description']
        self.wind_speed  = self.weather['list'][forecast_index]['wind']['speed']
        self.wind_dir    = self.weather['list'][forecast_index]['wind']['deg']
        self.visibility  = self.weather['list'][forecast_index]['visibility']
        self.date        = self.weather['list'][forecast_index]['dt_txt']

        self.update_k_to_f()
        self.data = {"City name": self.city_name,
                     "Time block": self.date,
                     "Weather description": self.description,
                     "Temperature": self.temp,
                     "Minimum Temperature": self.temp_min,
                     "Maximum Temperature": self.temp_max,
                     "Feels like": self.feels_like,
                     "Pressure": self.pressure,
                     "Humidity": self.humidity,
                     "Wind Speed": self.wind_speed,
                     "Wind Direction": self.wind_dir,
                     "Visibility": self.visibility}

    # --------------------------------------------------------------------------
    def update_k_to_f(self):
        """Run the kelvin to farenheit conversion function on our temp values."""
        self.temp = round(k_to_f(self.temp))
        self.temp_min = round(k_to_f(self.temp_min))
        self.temp_max = round(k_to_f(self.temp_max))
        self.feels_like = round(k_to_f(self.feels_like))

    # --------------------------------------------------------------------------
    def show_all_data(self):
        """ Show all the data we got from this block of weather forecast."""
        table = Table()
        table.add_column('Description')
        table.add_column('Data')

        with Live(table, refresh_per_second=4):
            for description, data in self.data.items():
                sleep(0.3)
                table.add_row(description, str(data))


# ------------------------------------------------------------------------------
# Functions --------------------------------------------------------------------
# ------------------------------------------------------------------------------
def request_weather_api(key: str) -> Response:
    """Request api from openweathermap.org. Return requests object if successful."""
    request = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?id={city_id}&APPID={key}")

    if request.status_code == accepted_response:
        return request
    elif request.status_code == unauthorized_response:
        console.print(errors.message_forbidden, style='red')
    else:
        console.print(f"\n\n\nResponse code is {request.status_code}. \n\n\n", style='red')


# ------------------------------------------------------------------------------
def save_json(request: Response, file_path: str):
    """Save the provided json file to given file_path."""
    with open(file_path, 'w') as file:
        json.dump(request.json(), file)


# ------------------------------------------------------------------------------
def open_json(file_path: str):
    """Open the json file in root folder. Return the json object."""
    try:
        with open(file_path) as file:
            json_data = json.load(file)
            return json_data
    except FileNotFoundError:
        print("Json file hasn't been created yet.")


# ------------------------------------------------------------------------------
def k_to_f(k: int) -> float:
    """Convert kelvin to fahrenheit, return result."""
    celsius = k - 273.15
    fahrenheit = (celsius * 1.8) + 32
    return fahrenheit


# ------------------------------------------------------------------------------
def verify_key_exists(key: str) -> str:
    """ Ensure user API key exists. If it does, return it."""
    if key is not None:
        # TODO: Help user automatically grab API key.
        return key
    else:
        raise errors.missing_api_exception


# ------------------------------------------------------------------------------
# TODO: This should probably be in a different file.
def color_shift(hex_value: hex, shift_amount: int) -> str:
    """Take a color hex value and add/subtract by given amount.
    Convert RBG hex value to RBG triplet value that rich can use.
    Return new color value."""
    # Hex values have a base of 16.
    hex_int = int(hex_value.lstrip('#'), 16)
    # Maximum color value is FFFFFF (255, 255, 255) RGB for non-HDR, ie: 16,777,215 as int.
    if hex_int + shift_amount > 16777215:
        # Our way of looping back around.
        new_color = hex((hex_int + shift_amount) - 16777215).lstrip('0x')
    else:
        new_color = hex(hex_int + shift_amount).lstrip('0x')
        # We need the hex value to always be 6 digits to be a valid color.
        while len(new_color) < 6:
            new_color = '0' + new_color

    return f"#{new_color}"


# ------------------------------------------------------------------------------
def temp_difference(start_temp: int, end_temp: int) -> str:
    # Show temp difference between two temperatures, rounded. Return message string.
    temp_adjust = round(end_temp - start_temp, 1)
    if temp_adjust <= 0:
        return f"{temp_adjust}° cooler at {end_temp}° F."
    elif temp_adjust > 0:
        return f"{temp_adjust}° warmer at {end_temp}° F."


# ------------------------------------------------------------------------------
def create_ui(now_input, timestamp=None):
    """ Create our user interface within the console. Returns the rich Layout."""

    # https://rich.readthedocs.io/en/latest/index.html
    # TODO: This is a messy function. Break it apart.
    now_temp = Text(str(weather_now.temp))
    now_wind = Text(str(weather_now.wind_speed))
    now_humidity = Text(str(weather_now.humidity))
    now_feels_like = Text(str(weather_now.feels_like))
    now_texts = [now_temp, now_wind, now_humidity, now_feels_like]

    for text in now_texts:
        text.stylize('bold magenta', 0, 6)

    ui = Layout()
    # TODO: Flesh out the UI more and fill with useful weather info.
    ui.split(
        Layout(name='left'),
        Layout(name='right'),
        direction='horizontal')

    ui['right'].split(
        Layout(name='3h'),
        Layout(name='6h'),
        Layout(name='9h'),
        direction='vertical')

    ui['left'].split(
        # "Now" panel, showing current weather info.
        Layout(
            Panel(
                f"Current temp: {now_input.temp}",
                box=box.DOUBLE,
                title=now_input.city_name),
            name='now',
            ratio=4),
        # "Info" panel, showing time until next update.
        Layout(
            Panel(
                get_next_update_time(timestamp),
                box=box.ASCII),
            name='info'),
        # Split direction for splitting "left" layout into "now" and "info" layouts.
        direction='vertical')

    return ui


# ------------------------------------------------------------------------------
def get_next_update_time(start_time):
    """Returns a string showing the next API update delay, and what time it will be."""
    update_delay_delta = timedelta(seconds=api_request_delay_in_seconds)
    next_update_time = start_time + update_delay_delta
    next_update_in_minutes = round(api_request_delay_in_seconds / min_in_sec)
    next_update_time_clean = next_update_time.strftime('%H:%M')
    message = f"Next update in {next_update_in_minutes} minutes at {next_update_time_clean}.\n\n"

    return message


# ------------------------------------------------------------------------------
# Start here.
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    key = verify_key_exists(my_key)

    while True:
        response = request_weather_api(key)
        save_json(response, file_name)
        weather_data = open_json(file_name)

        weather_now = WeatherAPIData(weather_data, 0)
        weather_03h = WeatherAPIData(weather_data, 1)
        weather_06h = WeatherAPIData(weather_data, 2)
        weather_09h = WeatherAPIData(weather_data, 3)
        weather_12h = WeatherAPIData(weather_data, 4)

        weather_blocks = [weather_12h, weather_09h, weather_06h, weather_03h, weather_now]

        current_time = datetime.now()
        interface = create_ui(weather_now, current_time)
        # The UI is actually drawn to the console here.
        console.print(interface)
        sleep(api_request_delay_in_seconds)
