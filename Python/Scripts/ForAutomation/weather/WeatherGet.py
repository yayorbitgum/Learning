# Pull from openweathermap.org to show me weather data in the console!
# Why not use my phone? Well I can just keep this up on my second monitor and
# take a peek at it every now and then get (somewhat) live updates without
# needing to refresh or open or touch anything.
# And it'll make me feel really cool and smart.
# https://openweathermap.org/forecast5
# Data is only updated once every 10 minutes on their servers.


# Imports ----------------------------------------------------------------------
import requests
import json
from config import my_key
# pprint is a bit simpler to make clean formats of json dumps for reading,
# for figuring out keys/values in these nested dictionaries the API gives.
from pprint import pprint
from time import sleep


# Variables --------------------------------------------------------------------
# reference "city.list.json" provided by openweathermap.org.
# You can pass in coordinates and other parameters, but IDs are more precise.
city_id = 4544349
file_name = f'{city_id}_weather.json'
delay = 1
sleepy_time = 600


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
    I'm just using Google here.
    Converting directly from K to F gave me differing temperature results.
    """
    celsius = k - 273.15
    fahrenheit = (celsius * 1.8) + 32
    return fahrenheit


def main():
    """
    Our loop to make requests and dig through the json file to display
    weather data we like.
    """
    while True:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?id={city_id}&APPID={my_key}")
        # Make sure we succeeded before we try to save it.
        if response.status_code == 200:
            # Save the request so we don't have to pull from API over and over.
            save_json(response)
            # Open the local save so we can play with data.
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
            # fut_feels_like  = round(k_to_f(fut_temps['feels_like']), 1)

            cur_humidity    = fut_temps['humidity']
            fut_humidity    = fut_temps['humidity']

            # Makes forecast temp change easier to digest.
            temp_adjust = round(fut_temperature - cur_temperature, 1)
            if temp_adjust < 0:
                fut_temp_text = f"{temp_adjust}° cooler at {fut_temperature}° F."
            elif temp_adjust > 0:
                fut_temp_text = f"{temp_adjust}° warmer at {fut_temperature}° F."

            # Pauses to add some motion to the data.
            print(f" ---------------- {city_name} --------------------------\n")
            sleep(delay)
            print(f"    {cur_description.capitalize()}!")
            sleep(delay)
            print(f"    {cur_humidity}% humidity.")
            sleep(delay)
            print(f"    {cur_temperature}° F: Current temperature.")
            sleep(delay)
            print(f"    {cur_feels_like}° F: Feels like this.\n")
            sleep(delay)
            print(f"  ------------------------------------------------------\n")
            sleep(delay)
            print(f"Coming up in 3 hours..\n")
            sleep(delay)
            print(f"    {fut_description.capitalize()} soon!")
            sleep(delay)
            print(f"    {fut_humidity}% humidity.")
            sleep(delay)
            print(f"    {fut_temp_text}")
            sleep(delay)
            print(f"  ------------------------------------------------------\n")
            sleep(delay)

            print(f"Waiting {sleepy_time/60} minutes.\n\n")

        else:
            print(f"\n\n\nResponse code is {response.status_code}. \n\n\n")

        # Wait this long before querying again.
        sleep(sleepy_time)


# Program-----------------------------------------------------------------------
main()
