# Pull from openweathermap.org to display current weather forecasts.
# https://openweathermap.org/forecast5

# TODO: Automate grabbing API key.
# TODO: Automate grabbing city.list.json, and decompressing.
# ------------------------------------------------------------------------------
# Imports ----------------------------------------------------------------------
# ------------------------------------------------------------------------------
import os
import requests
import json
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
api_request_delay_in_seconds = 600
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
        self.date        = self.weather['list'][forecast_index]['dt_txt']

        self.update_k_to_f()
        self.data = {"City name": self.city_name,
                     "Time block": self.date,
                     "Weather description": self.description,
                     "Temperature": self.temperature,
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
        """
        This method runs the kelvin to farenheit conversion function
        on our temperature values.
        """
        self.temperature       = round(convert_k_to_f(self.temperature))
        self.temp_min   = round(convert_k_to_f(self.temp_min))
        self.temp_max   = round(convert_k_to_f(self.temp_max))
        self.feels_like = round(convert_k_to_f(self.feels_like))

    # --------------------------------------------------------------------------
    def show_all_data(self):
        """ Show all the data we got from this block of weather forecast."""
        table = Table()
        table.add_column('Description')
        table.add_column('Data')

        with Live(table, refresh_per_second=4):
            for description, data in self.data.items():
                table.add_row(description, str(data))


# ------------------------------------------------------------------------------
# Functions --------------------------------------------------------------------
# ------------------------------------------------------------------------------
def request_weather_api(api_key: str, api_city_id=None) -> (Response, str):
    """
    Request api from openweathermap.org.
    Return tuple of requests object, and specific city id if successful.
    https://openweathermap.org/current
    """

    # We need to make a different API request depending on if we have basic
    # user search term, or if we've acquired the specific city id.
    if api_city_id is not None:
        request = requests.get(f"http://api.openweathermap.org/data/2.5/forecast"
                               f"?id={api_city_id}"
                               f"&APPID={api_key}")
    else:
        request = requests.get(f"http://api.openweathermap.org/data/2.5/forecast"
                               f"?q={location}"
                               f"&APPID={api_key}")

    # 200 ----------------------------------------------------------------------
    if request.status_code == accepted_code:
        request_and_id = [request, api_city_id]
        return request_and_id

    # 401 ----------------------------------------------------------------------
    elif request.status_code == unauth_code:
        console.print(errors.message_forbidden, style='red')

    # 404 ----------------------------------------------------------------------
    elif request.status_code == not_found_code:
        # Openweathermap's API does not partial matching, so often rejects input.
        # So let's try our own very slow fuzzy matching locally!
        # TODO: Maybe this would be a good time to practice making my own API
        # and just have a server host the city.list.json, to give us back the id.
        console.print('[red]Did you mean...[/]')
        console.print('[grey0][italic]Searching for closest matches...[/][/]')

        # Fuzzy results selection. ---------------------------------------------
        choices = fuzzy_find_city(location)
        for index, choice in enumerate(choices):
            console.print(f"{index}: {choice}")

        try:
            selection = int(input('Choose option number: '))
            location_string = choices[selection]
        except (IndexError, ValueError):
            # We'll default to first option for now. TODO: Ask for input again.
            location_string = choices[0]

        city, state, api_city_id = location_string.split(',')
        api_city_id = api_city_id.strip()

        # ----------------------------------------------------------------------
        # Now that we've got the exact city id, let's request API again.
        return request_weather_api(my_key, api_city_id)

    else:
        console.print(f'[red] Response code {request.status_code}![/]')


# ------------------------------------------------------------------------------
def save_json(request, file_path: str):
    """Save the provided json file to given file_path."""
    if request is not None:
        with open(file_path, 'w') as file:
            json.dump(request.json(), file)


# ------------------------------------------------------------------------------
def open_json(file_path: str):
    """Open the json file in root folder. Return the json object."""
    try:
        with open(file_path, encoding='utf8') as file:
            json_data = json.load(file)
            return json_data
    except FileNotFoundError:
        print("Json file hasn't been created yet.")


# ------------------------------------------------------------------------------
def convert_k_to_f(k: int) -> float:
    """Convert kelvin to fahrenheit, return result."""
    celsius = k - 273.15
    fahrenheit = (celsius * 1.8) + 32
    return fahrenheit


# ------------------------------------------------------------------------------
def verify_key_exists(key_to_verify: str) -> str:
    """ Ensure user API key exists. If it does, return it."""
    if key_to_verify is not None:
        return key_to_verify
    else:
        raise errors.missing_api_exception


# ------------------------------------------------------------------------------
def shift_color(hex_value: hex, shift_amount: int) -> str:
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
        return f"{temp_adjust}°F cooler."
    elif temp_adjust > 0:
        return f"{temp_adjust}°F warmer."


# ------------------------------------------------------------------------------
def color_by_temperature(temperature: int) -> str:
    """Take in temperature value and return text with color tags for use with rich ui."""
    # Color reference: https://rich.readthedocs.io/en/latest/_modules/rich/color.html
    temperature_breakpoints = [0, 32, 50, 65, 79, 89, 101, 115]
    temperature_colors = ["blue_violet",
                          "deep_sky_blue1",
                          "cyan",
                          "green",
                          "yellow",
                          "orange4",
                          "red",
                          "magenta",
                          "bright_magenta"]
    bisect_index = bisect(temperature_breakpoints, temperature)
    color = temperature_colors[bisect_index]
    # Colors are assigned within strings like HTML tags, with [brackets][/brackets].
    return f"[{color}]{temperature}°F[/]"


# ------------------------------------------------------------------------------
def wind_degrees_to_direction(degrees: int) -> str:
    """Convert input degrees (int) to and return cardinal direction (str)."""
    breakpoints = [0, 5, 85, 95, 175, 185, 265, 275, 355, 360]
    directions = ["North", "North",
                  "Northeast", "East", "Southeast", "South",
                  "Southwest", "West", "Northwest", "North", "North"]

    bisect_index = bisect(breakpoints, degrees)
    direction = directions[bisect_index]
    return direction


# ------------------------------------------------------------------------------
def create_weather_panel(weather: WeatherAPIData) -> Panel:
    """ Take in WeatherAPIData instance. Return rich Panel with weather info."""
    # Temperature color tagging.
    current_colored = color_by_temperature(weather.temperature)
    feels_colored = color_by_temperature(weather.feels_like)
    # N E S W text.
    wind_cardinal = wind_degrees_to_direction(weather.wind_dir)
    panel_text = (f"{current_colored} with {weather.description.title()}\n"
                  f"Feels like {feels_colored}\n"
                  f"{wind_cardinal} @ [cyan]{weather.wind_speed}mph[/]\n"
                  f"Humidity @ [cyan]{weather.humidity}%[/]\n")

    title = weather.date
    panel = Panel(panel_text, box=box.ASCII, title=title)
    return panel


# ------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------
def create_ui(timestamp: datetime):
    """ Create our user interface within the console. Returns the rich Layout."""
    # https://rich.readthedocs.io/en/latest/index.html
    ui = Layout()
    ui.split(
        Layout(name='left'),
        Layout(name='right'),
        direction='horizontal')

    panel_now = create_weather_panel(weather_now)
    panel_3h = create_weather_panel(weather_03h)
    panel_6h = create_weather_panel(weather_06h)
    panel_9h = create_weather_panel(weather_09h)
    panel_info = Panel(f"[i]{get_next_update_time(timestamp, api_request_delay_in_seconds)}[/]")

    state_code = determine_state_code(city_list_filepath, weather_now.id)
    if state_code:
        panel_now.title = f"[yellow]{weather_now.city_name}, {state_code}, {weather_now.country}[/]"
    else:
        panel_now.title = f"[yellow]{weather_now.city_name}, {weather_now.country}[/]"

    lat = weather_now.latitude
    lon = weather_now.longitude
    panel_now.renderable += f"[i]\nPopulation: {weather_now.population:,}[/]"
    panel_now.renderable += f"[i]\nGPS: [link=https://www.google.com/maps/@{lat},{lon}]{lat}, {lon}[/link][/]"
    panel_3h.title = f"[yellow]3 Hours[/]"
    panel_6h.title = f"[yellow]6 Hours[/]"
    panel_9h.title = f"[yellow]9 Hours[/]"

    # Add temperature differences to forecast panels.
    temp_diff_3h = temp_difference(weather_now.temperature, weather_03h.temperature)
    temp_diff_6h = temp_difference(weather_now.temperature, weather_06h.temperature)
    temp_diff_9h = temp_difference(weather_now.temperature, weather_09h.temperature)
    panel_3h.renderable += f"{temp_diff_3h}"
    panel_6h.renderable += f"{temp_diff_6h}"
    panel_9h.renderable += f"{temp_diff_9h}"

    panel_now.box = box.DOUBLE
    panel_info.box = box.ASCII

    # Future forecast panels.
    ui['right'].split(
        Layout(panel_3h, name='3h'),
        Layout(panel_6h, name='6h'),
        Layout(panel_9h, name='9h'),
        direction='vertical')

    # "now" and "info" panels.
    ui['left'].split(
        Layout(panel_now, name='now', ratio=4),
        Layout(panel_info, name='info'),
        direction='vertical')

    return ui


# ------------------------------------------------------------------------------
def get_next_update_time(start_time, delay_in_seconds):
    """Returns a string showing the next API update delay, and what time it will be."""
    next_update_time = start_time + timedelta(seconds=delay_in_seconds)
    next_update_in_minutes = round(delay_in_seconds / min_in_sec)
    next_update_text = next_update_time.strftime('%H:%M')

    message = (f"Next update in {next_update_in_minutes} minutes "
               f"at {next_update_text.lstrip('0')}")

    return message


# ------------------------------------------------------------------------------
def clear_old_json():
    """Check for and delete old files from previous script runs generated in json_files."""
    json_file_list = [file for file in os.listdir('json_files') if file.endswith('json')]

    if json_file_list:
        console.print(f"[grey0 italic] Deleting old files generated by WeatherGet...[/]")

        for file in json_file_list:
            os.remove(os.path.join('json_files', file))
            console.print(f"[red]Removed {file} from 'json_files' folder.[/red]")


# ------------------------------------------------------------------------------
def create_json_folder():
    try:
        os.mkdir(json_folder_path)
    except FileExistsError:
        console.print('[grey0 italic]Found json_files folder.[/]')


# ------------------------------------------------------------------------------
# Start here.
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    create_json_folder()
    clear_old_json()
    location = input('Enter location: ').title()
    weather_api_file_name = f'{json_folder_path}/{location}.json'
    key = verify_key_exists(my_key)
    # request_weather_api will give us (API Response, city_id).
    response = request_weather_api(key)
    city_id = response[1]

    while True:
        save_json(response[0], weather_api_file_name)
        weather_data = open_json(weather_api_file_name)
        weather_now = WeatherAPIData(weather_data, 0)
        weather_03h = WeatherAPIData(weather_data, 1)
        weather_06h = WeatherAPIData(weather_data, 2)
        weather_09h = WeatherAPIData(weather_data, 3)

        current_time = datetime.now()
        interface = create_ui(current_time)
        console.print(interface)

        sleep(api_request_delay_in_seconds)
        response = request_weather_api(key, city_id)
