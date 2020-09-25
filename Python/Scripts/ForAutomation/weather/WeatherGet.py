# Pull from openweathermap.org to show me weather data in the console!
# Why not use my phone? Well I can just keep this up on my second monitor and
# take a peek at it every now and then get (somewhat) live updates without
# needing to refresh or open or touch anything.
# And it'll make me feel really cool and smart.
# https://openweathermap.org/appid
# https://openweathermap.org/api/weather-map-2
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
delay = 0.25
# Setting to 60 seconds for testing, but don't need faster than 600.
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
            # Open the local save so we can view data.
            weather = open_json()
            # After a lot of trial and error, I found where the info is stored.
            # weather['list'][0]['main'] leads to:
            #   'feels like'
            #   'humidity'
            #   'pressure'
            #   'temp'
            # and others.

            city_name   = weather['city']['name']
            description = weather['list'][0]['weather'][0]['description']
            tmps        = weather['list'][0]['main']

            # Convert temps to F, then round up decimal points to 1.
            temperature = round(k_to_f(tmps['temp']), 1)
            feels_like  = round(k_to_f(tmps['feels_like']), 1)
            humidity    = tmps['humidity']

            # Pauses to add some motion to the data.
            print(f" ---------------- {city_name} --------------------------")
            sleep(delay)
            print(f"    {description.capitalize()}!")
            sleep(delay)
            print(f"    {humidity}% humidity.")
            sleep(delay)
            print(f"    {temperature}° F: Current temperature.")
            sleep(delay)
            print(f"    {feels_like}° F: Feels like this.")
            sleep(delay)
            print(f"  --------------------------------------------------------")
            sleep(delay)
            print(f"\n\nWaiting {sleepy_time} seconds.\n\n")

        else:
            print(f"\n\n\nResponse code is {response.status_code}. \n\n\n")

        # Wait this long before querying again.
        sleep(sleepy_time)


# Program-----------------------------------------------------------------------
main()
