# Keeps track of current International Space Station location, and checks to see if it's above me or nearby.
#
# Initially started as practicing requests but then I found a neat API for the ISS.
# http://api.open-notify.org/
#
# Every link and resource I come across is just the result of Googling.


# //////////////////////////////////////////// Imports ////////////////////////////////////////////
# For going through large data files very quickly without needing a server or ridiculous amounts of RAM.
# https://github.com/vaexio/vaex
# https://www.christopherlovell.co.uk/blog/2016/04/27/h5py-intro.html
# from zipfile import ZipFile
# import pandas as pd
# import h5py
# import vaex

# And then my stuff.
import requests
import math
from time import sleep as pause
from datetime import datetime as dt
from geodata_parser import get_data_details as get_geodata
import csv
import mmap


# //////////////////////////////////////////// Static Functions ////////////////////////////////////////////
def format_lng_direction(longitude_input):
    """
    :param longitude_input: Take in the longitude and
    :return: return the direction as a string; East, West, or right on the Prime Meridian.
    """
    direction = ''

    if longitude_input > 0:
        direction = 'East'
    elif longitude_input < 0:
        direction = 'West'
    elif longitude_input == 0:
        direction = 'on the Prime Meridian'

    return direction


def format_lat_direction(latitude_input):
    """
    :param latitude_input: Take in the latitude and
    :return: return the direction as a string; North, South, or right on the Equator.
    """
    direction = ''

    if latitude_input > 0:
        direction = 'North'
    elif latitude_input < 0:
        direction = 'South'
    elif latitude_input == 0:
        direction = 'on the Equator'

    return direction


def set_update_rate():
    """
    Takes user input, just for setting how often we ping for ISS location.
    """
    try:
        rate = float(input("Please enter your preferred update rate in seconds, "
                           "then hit enter to start tracking:\n"))
        print(f"Your update rate is set to once per {rate} seconds.\n")
        return rate

    except ValueError:
        print("\nWell, since you didn't enter a number, I'll just set it to 1 second.\n")
        pause(3)
        return 1


# //////////////////////////////////////////// Classes ////////////////////////////////////////////
class ISSTracking:
    """
    This class will track the ISS with requests from external API,
    check distance between ISS and OKC,
    format updates automatically and print,
    TODO: show the current geographical location of the ISS based on current coordinates.
    """
    def __init__(self):
        self.longitude = 0
        self.latitude = 0
        self.start_time = None
        self.current_time = None
        self.okc_long = 35.4676
        self.okc_lat = 97.5164

    def elapsed_time(self):
        """
        Returns the time elapsed since we started tracking.
        """
        elapsed = dt.now() - self.start_time
        return elapsed

    def get_distance(self):
        """
        Can I find the actual distance between two coordinates?
        Maybe I could show how close the ISS is to me?
        Well let's see what Google says and do what they say to do. Learn and copy and paste.
        https://kite.com/python/answers/how-to-find-the-distance-between-two-lat-long-coordinates-in-python
        """

        # Radians are the angle made when a radius is wrapped around a circle.
        # The earth is round (for the most part), so this should work.
        # https://www.mathsisfun.com/geometry/radians.html
        okc_long_rad = math.radians(self.okc_long)
        okc_lat_rad = math.radians(self.okc_lat)
        iss_long_rad = math.radians(self.longitude)
        iss_lat_rad = math.radians(self.latitude)

        # This is measured in kilometers.
        radius_of_earth = 6378

        # Now get the difference between the coordinates.
        diff_long = iss_long_rad - okc_long_rad
        diff_lat = iss_lat_rad - okc_lat_rad

        # Now we copy and paste the Haversine Formula that I don't understand at all, and input our coordinates.
        a = math.sin(diff_lat / 2) ** 2 + math.cos(okc_lat_rad) * math.cos(iss_lat_rad) * math.sin(diff_long / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = radius_of_earth * c
        # That gave me a long number with a lot of decimals, so I'm gonna round it up.
        # https://www.geeksforgeeks.org/round-function-python/
        distance_clean = round(distance, 2)
        # Now we return the distance.
        return distance_clean

    def check_distance(self):
        """
        We'll use the get_distance_miles(), and check the distance each tick, and timestamp it.
        """
        current_distance = self.get_distance()
        # If the distance between the center of my sky, and the ISS is less than 1000 km:
        # 600km is about the length of Oklahoma, so maybe 1000km is a nice round number for easy spotting.
        if current_distance < 1000:
            print(f"The ISS is flying over Oklahoma right now, just about!")
            print(f"Currently the ISS is about {current_distance} kilometers from the center of your sky.\n")

        else:
            print(f"The ISS is {current_distance:,} kilometers away from OKC.")
            # Maybe later I could have it show what location it's above based on coordinates.
            # Format North/South/East/West based on whether lng/lat are positive or negative.
            # Example: "Current coordinates: 10° North by 80° East".
            print(f"Current coordinates: "
                  f"{self.latitude}° {format_lat_direction(self.latitude)} by "
                  f"{self.longitude}° {format_lng_direction(self.longitude)}.\n")

    def get_iss_loc_name(self):
        """
        Get the geodata values.
        We'll pass in the opened reader file, and the coordinates.
        """
        print("\nChecking location data. This might take a minute...")
        location_data_result = get_geodata(reader, self.latitude, self.longitude)

        # If location data coming back is not empty:
        if location_data_result is not None:
            print(f"\nThe ISS is currently flying over {location_data_result}!\n")

        else:
            # Eventually we'll check the global data too.
            print("\n The ISS is currently flying somewhere away from the US.\n"
                  "----------------------------------------------------------\n")

    def start_request_and_update(self):
        """
        Set update rate, set starting date-timestamp, and then run requests loop until we quit.
        """
        print("This program will keep running until you close it.")

        # Set how fast we want to update. I don't think the API updates any faster than 0.5s.
        update_rate = set_update_rate()
        # Set the current time as the start_time timestamp as soon as we start requesting.
        self.start_time = dt.now()
        # Establish ping count for notifying user with time elapsed later.
        ping_count = 0

        while True:
            # Get the iss-now info response. Should be response 200 if all is well.
            # I found a nice big list of response codes here for debugging:
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
            iss_response = requests.get("http://api.open-notify.org/iss-now.json")

            # We can tell it's a json file in the URL, so convert the response to json object.
            iss_json = iss_response.json()
            # Make a copy of the json object as a dictionary, since that's all it seems to be.
            # Then we can work with the dictionary more easily, with dictionary functions.
            iss_dict = dict(iss_json)

            # I could also get the status code directly with "iss_response.status_code".
            status = iss_dict.get("message")

            if status == "success":
                # Now we pick apart the nested dictionaries to get the positions we want.
                # We can see Longitude and Latitude are nested inside "iss_position" dictionary.
                # So let's get that one first. I forgot how to get keys from dictionaries, so I Googled.
                # https://www.geeksforgeeks.org/get-method-dictionaries-python/
                iss_pos = iss_dict.get("iss_position")

                # Then from that, grab the values for these keys, and make them floats so we can use them as numbers.
                # The strings need to be converted to floats because they're numbers like "32.9035".
                self.longitude = float(iss_pos.get("longitude"))
                self.latitude = float(iss_pos.get("latitude"))

                # Check and display the current distance.
                self.check_distance()
                # Update ping counter.
                ping_count += 1
                # Pause for a bit before pinging again.
                pause(update_rate)

            else:
                print(f"Update failed! Received message: {status}. Retrying...")

            # Once every 20 pings:
            if ping_count % 20 == 0:
                # Show current time and time elapsed since we started.
                print(f"/////////////// Time elapsed: {self.elapsed_time()}\n"
                      f"/////////////// Current datetime: {dt.now()}\n")

                # This is where we'll show the current location name.
                # At least be in range of the length of the entire US before we check the big USA list haha.
                if self.get_distance() < 4313:
                    iss.get_iss_loc_name()


# //////////////////////////////////////////// Program ////////////////////////////////////////////

# For now, we'll just work with the US-based data set.
national_file = 'GeoLocationInfo/NationalFile_20200501.txt'
# Had to set encoding to utf-8, probably because they're text files. I ran into this on my Word Counter project.
# We'll leave the file open..
file = open(national_file, encoding='utf-8')
# And map it to memory, ie store it all in RAM. 0 means the whole file into memory, in reading mode. I hope.
# https://stackoverflow.com/questions/11159077/python-load-2gb-of-text-file-to-memory
file_mapped = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
# Make the csv reader object.
# Since the delimiters are | instead of commas, I can set that here in the reader.
# https://realpython.com/python-csv/#optional-python-csv-reader-parameters
reader = csv.reader(file_mapped, delimiter='|')

iss = ISSTracking()
iss.start_request_and_update()
