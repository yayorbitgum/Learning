# Keeps track of current International Space Station location,
# and checks to see if it's above me or nearby.
#
# Initially started as practicing requests but then I found
# a neat API for the ISS.
# http://api.open-notify.org/


# Imports ----------------------------------------------------------------------
import requests
import math
import pyfiglet
from time import sleep as pause
from datetime import datetime as dt
from geodata_scanner import LocationDataFrames


# Variables --------------------------------------------------------------------
folder_name = 'GeoLocationInfo/hdf5'
national_file_path = f'{folder_name}/NationalFile_20200501.hdf5'

global_files_list = [f'{folder_name}/Countries_administrative_a.hdf5',
                     f'{folder_name}/Countries_hydrographic_h.hdf5',
                     f'{folder_name}/Countries_hypsographic_t.hdf5',
                     f'{folder_name}/Countries_localities_l.hdf5',
                     f'{folder_name}/Countries_populatedplaces_p.hdf5',
                     f'{folder_name}/Countries_spot_s.hdf5',
                     f'{folder_name}/Countries_transportation_r.hdf5',
                     f'{folder_name}/Countries_undersea_u.hdf5',
                     f'{folder_name}/Countries_vegetation_v.hdf5']


# Static Functions -------------------------------------------------------------
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
    Let user set update rate for location ping.
    """
    try:
        rate = float(input("Please enter your preferred update rate in seconds, "
                           "then hit enter to start tracking:\n"))
        print(f"Your update rate is set to once per {rate} seconds.\n")
        return rate

    except ValueError:
        print("\nYou didn't enter a number. Update rate set to 5 seconds.\n")
        pause(1)
        return 5


# //////////////////////////////////////////// Classes ////////////////////////////////////////////
class ISSTracking:
    """
    This class will track the ISS with requests from external API,
    ccheck distance between ISS and our user input location,
    format updates automatically and print, and
    show the current geographical location of the ISS based on current coordinates.
    """
    def __init__(self):
        self.latitude = 0
        self.longitude = 0
        self.start_time = None
        self.current_time = None
        self.my_long = 0.0
        self.my_lat = 0.0
        self.loc_scan_count = 0
        self.loc_df = LocationDataFrames(self.latitude, self.longitude)

    def get_location_input(self):
        """ Have the user input their own coordinates for distance tracking."""

        try:
            self.my_lat = float(input("Enter the latitude for your current location (in decimal form):\n").strip())
            self.my_long = float(input("Enter your longitude too (in decimal form):\n").strip())

        except (TypeError, ValueError):
            # Reset the values and try again.
            self.my_lat = 0.0
            self.my_long = 0.0
            print("That didn't work.. "
                  "Make sure you enter a number for your longitude or latitude. "
                  "For example: 34.5003\n")
            self.get_location_input()

        # If that didn't give us an error, let's keep going.
        print(f"Great! Your input coordinates are "
              f"{self.my_lat}° {format_lat_direction(self.my_lat)} by "
              f"{self.my_long}° {format_lng_direction(self.my_long)}.\n")
        pause(0.5)
        # Now we try to show the user where they say they are, based on the database matches.
        self.get_user_loc_name()
        pause(1.5)

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
        my_long_rad = math.radians(self.my_long)
        my_lat_rad = math.radians(self.my_lat)
        iss_long_rad = math.radians(self.longitude)
        iss_lat_rad = math.radians(self.latitude)

        # This is measured in kilometers.
        radius_of_earth = 6378

        # Now get the difference between the coordinates.
        diff_long = iss_long_rad - my_long_rad
        diff_lat = iss_lat_rad - my_lat_rad

        # Now we copy and paste the Haversine Formula that I don't understand at all, and input our coordinates.
        a = math.sin(diff_lat / 2) ** 2 + math.cos(my_lat_rad) * math.cos(iss_lat_rad) * math.sin(diff_long / 2) ** 2
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
        if current_distance < 1000:
            print(f"The ISS is flying over you right now, just about!")
            print(f"Currently it's about {current_distance} kilometers from the center of your sky.\n")

        else:
            print(f"The ISS is {current_distance:,} kilometers away from your location.")
            # Maybe later I could have it show what location it's above based on coordinates.
            # Format North/South/East/West based on whether lng/lat are positive or negative.
            # Example: "Current coordinates: 10° North by 80° East".
            print(f"Current coordinates: "
                  f"{self.latitude}° {format_lat_direction(self.latitude)} by "
                  f"{self.longitude}° {format_lng_direction(self.longitude)}.\n")

    def get_user_loc_name(self):
        """
        Get the geodata values so we can see what place the user has input.
        We'll pass in the user input coordinates.
        The dataframes are opened and scanned in geodata_scanner.py.
        """
        usa_results = self.loc_df.scan_usa_df(self.my_lat, self.my_long)
        global_pop_result = self.loc_df.scan_global_pop_df(self.my_lat, self.my_long)

        if usa_results is not None:
            usa_feature = usa_results[0]
            usa_state = usa_results[1]
            usa_elevation = usa_results[2]
            print(f"Based on your coordinates, "
                  f"you should be at or near {usa_feature} in {usa_state}, "
                  f"with an elevation of {usa_elevation}m.\n")

        elif usa_results is None:
            # So if USA scan got us nothing, now we check the global dataframe.
            if global_pop_result is not None:
                print(f"Based on your coordinates, you should be at or near {global_pop_result}.\n")

        else:
            print("Well, to be honest I'm not sure where that is, but hey let's"
                  " start trackin!\n")

    def get_iss_loc_name(self):
        """
        Get the geodata values so we can see what place the ISS is above.
        We'll pass in the current coordinates.
        The dataframes are opened and scanned in geodata_scanner.py.
        """

        # This is where we pass in the current ISS coordinates to be checked against the
        # location dataframes we've set up and converted.
        usa_results = self.loc_df.scan_usa_df(self.latitude, self.longitude)
        global_pop_result = self.loc_df.scan_global_pop_df(self.latitude, self.longitude)

        if usa_results is not None:
            # scan_usa_df() returns a list of three things: feature, state, and elevation.
            usa_feature = usa_results[0]
            usa_state = usa_results[1]
            usa_elevation = usa_results[2]
            # And print it!
            print(f"The ISS is flying over {usa_feature} in {usa_state}. "
                  f"The local elevation is {usa_elevation}.\n")

        elif usa_results is None:
            # So if USA scan got us nothing, now we check the global dataframe.
            if global_pop_result is not None:
                print(f"The ISS is flying over {global_pop_result}.")

    def start_request_and_update(self):
        """
        Start geodata scanner and load up our hdf5 dataframes,
        set update rate, set starting date-timestamp, and then run requests loop until we quit.
        """
        print(pyfiglet.figlet_format("ISS Tracker", font='alligator2'))
        # Start process of loading our hdf5 files into dataframes.
        self.loc_df.startup_load()
        # Make sure we only get input after loading the databases.
        self.get_location_input()

        # Continue after.
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

            # This is where we'll show the current location name.
            iss.get_iss_loc_name()

            # Once every 20 pings:
            if ping_count % 20 == 0:
                # Show current time and time elapsed since we started.
                print(f"\n/////////////// Time elapsed: {self.elapsed_time()}\n"
                      f"/////////////// Current datetime: {dt.now()}\n")


# //////////////////////////////////////////// Program ////////////////////////////////////////////
# Instantiate.
iss = ISSTracking()
# Start!
iss.start_request_and_update()
