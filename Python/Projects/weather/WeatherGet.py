# Pull from openweathermap.org to current weather and the weather in the next 3 hours.
# https://openweathermap.org/forecast5


# Imports ----------------------------------------------------------------------
import requests
import json
from config import my_key
from time import sleep
from datetime import datetime, timedelta


# Variables --------------------------------------------------------------------
# reference "city.list.json" provided by openweathermap.org.
# You can pass in coordinates and other parameters, but IDs are more precise.
city_id = 4544349
file_name = f'{city_id}_weather.json'
animation_delay = 1
min_in_sec = 60
accepted_response = 200
# Data is only updated once every 10 minutes on their servers.
api_request_delay_in_seconds = 600


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


def k_to_f(k):
    """
    Converts kelvin to celsius, then to fahrenheit. Pass in kelvin first.
    Converting directly from K to F gave me differing temperature results.
    I don't understand why. Yet.
    """
    celsius = k - 273.15
    fahrenheit = (celsius * 1.8) + 32
    return fahrenheit


def main():
    """
    Main loop to make requests and dig through the json file to display
    weather data we want.
    """
    while True:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?id={city_id}&APPID={my_key}")
        # Make sure we succeeded before we try to save it.
        if response.status_code == accepted_response:
            # Save the request so we don't have to pull from API over and over.
            save_json(response)
            weather = open_json()
            city_name   = weather['city']['name']
            # ['list'][0] is current weather.
            # ['list'][1], or [2], etc would be forecast.
            # Each new list is 3 hours forecast ahead of last list. There are 40.

            # Current: [0]
            cur_description = weather['list'][0]['weather'][0]['description']
            cur_temps       = weather['list'][0]['main']

            # 3 hours from now: [1]
            fut_description = weather['list'][1]['weather'][0]['description']
            fut_temps       = weather['list'][1]['main']

            # Convert temps to F, then round up decimal points to 1.
            cur_temperature = round(k_to_f(cur_temps['temp']), 1)
            cur_feels_like  = round(k_to_f(cur_temps['feels_like']), 1)
            fut_temperature = round(k_to_f(fut_temps['temp']), 1)

            cur_humidity    = fut_temps['humidity']
            fut_humidity    = fut_temps['humidity']

            # Makes forecast temp change easier to digest.
            temp_adjust = round(fut_temperature - cur_temperature, 1)
            if temp_adjust < 0:
                fut_temp_text = f"{temp_adjust}° cooler at {fut_temperature}° F."
            elif temp_adjust > 0:
                fut_temp_text = f"{temp_adjust}° warmer at {fut_temperature}° F."

            # Add some motion to the data, rather than blasting you with everything
            # at once.
            readout_lines = [f" ---------------- {city_name} --------------------------\n",
                              f"    {cur_description.capitalize()}.",
                              f"    {cur_humidity}% humidity.",
                              f"    {cur_temperature}° F current temp.",
                              f"    {cur_feels_like}° F feeling.\n",
                              f"------------------------------------------------------\n",
                              f"Coming up in 3 hours:\n",
                              f"    {fut_description.capitalize()}.",
                              f"    {fut_humidity}% humidity.",
                              f"    {fut_temp_text}",
                              f"------------------------------------------------------\n"]

            for line in readout_lines:
                print(line)
                sleep(animation_delay)

            time = datetime.now()
            update_delay_delta = timedelta(seconds=api_request_delay_in_seconds)
            next_update_time = time + update_delay_delta

            print(f"Next update in {round(api_request_delay_in_seconds / min_in_sec)} "
                  f"minutes at {next_update_time.strftime('%H:%M')}.\n\n")

        else:
            print(f"\n\n\nResponse code is {response.status_code}. \n\n\n")

        # Wait this long before querying again.
        sleep(api_request_delay_in_seconds)


# Program-----------------------------------------------------------------------
main()
