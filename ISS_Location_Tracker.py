# Keeps track of current International Space Station location, and checks to see if it's above me or nearby.
# Initially started as practicing requests but then I found a neat API for the ISS.
# http://api.open-notify.org/
# Still a work in progress!

# //////////////////////////////////////////// Imports ////////////////////////////////////////////
import requests
import math
from time import sleep as pause


# //////////////////////////////////////////// Functions ////////////////////////////////////////////
def get_distance_miles():
    """
    Can I find the actual distance between two coordinates?
    Maybe I could show how close the ISS is to me?
    Well let's see what Google says and do what they say to do. Ala copy and paste.
    https://kite.com/python/answers/how-to-find-the-distance-between-two-lat-long-coordinates-in-python
    """

    # Radians are the angle made when a radius is wrapped around a circle.
    # The earth is round (for the most part), so this should work.
    # https://www.mathsisfun.com/geometry/radians.html
    okc_long_rad = math.radians(okc_long)
    okc_lat_rad = math.radians(okc_lat)
    iss_long_rad = math.radians(longitude)
    iss_lat_rad = math.radians(latitude)

    # This is measured in Freedom Units (miles). We could always convert later lol.
    # Since I'm entering the radius of the earth in miles, I'm assuming my distance result will be miles too.
    # Hopefully.
    radius_of_earth = 3958.8

    # Now get the difference between the coordinates.
    diff_long = iss_long_rad - okc_long_rad
    diff_lat = iss_lat_rad - okc_lat_rad

    # Now we copy and paste the Haversine Formula that I don't understand at all, and input our coordinates.
    # I think "a" stands for arc, but not sure.
    # I'm confused why we use the two latitudes, but only the longitude difference. But again I don't understand this.
    a = math.sin(diff_lat / 2) ** 2 + math.cos(okc_lat_rad) * math.cos(iss_lat_rad) * math.sin(diff_long / 2) ** 2
    # "c" probably stands for circle. Again, not sure.
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius_of_earth * c

    # That gave me a long number with a lot of decimals, so I'm gonna round it up.
    # https://www.geeksforgeeks.org/round-function-python/
    distance_clean = round(distance, 2)
    # Now we return the distance.
    return distance_clean


def check_distance_dumb():
    """
    This is some arbitrary means of seeing if ISS might be in view.
    I just roughly guessed based on a map of the US that shows long/lat lines.
    """

    # We can check to see if the ISS coordinates are within 10 degrees of my current location.
    # Looking at a map, longitude within 10-15 degrees is more or less straight above.
    # Latitude within 15-20 degrees is roughly about the same.
    if iss_longitude_vicinity < 15 and iss_latitude_vicinity < 20:
        print("Hey the ISS is flying over you right now!")
        print(f"It's currently about {abs(iss_latitude_vicinity - iss_longitude_vicinity)} degrees away!"
              f"\nYea, that makes no sense I know. Just look at the sky somewhere.")


def check_distance_smart():
    """
    This one makes more sense.
    We'll use the get_distance_miles() that uses a real formula.
    """
    current_distance = get_distance_miles()
    # If the distance between the center of my sky, and the ISS is less than 400 miles:
    # 400 miles is about the length of Oklahoma, because why not.
    if current_distance < 400:
        print(f"\nThe ISS is flying over Oklahoma right now, just about!")
        print(f"Currently the ISS is about {current_distance} miles from the center of your sky.")

    else:
        print(f"\nThe ISS is {current_distance:,} miles away from OKC.")
        # Maybe later I could have it show what location it's above based on coordinates.
        print(f"It's current coordinates are {longitude} degrees N/S by {latitude} degrees E/W.")


# //////////////////////////////////////////// Requests/Program ////////////////////////////////////////////
input("This program will keep running until you close it. Hit enter to start tracking...")

# My current location, roughly. I'm sure I could automate this later for custom input.
# Someone somewhere has a list of coordinates you can pull for cities/countries, surely.
okc_long = 35.4676
okc_lat = 97.5164


while True:
    # Get the iss-now info response. Should be response 200 if all is well.
    # I found a nice big list of response codes here for debugging:
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    response = requests.get("http://api.open-notify.org/iss-now.json")

    # We can tell it's a json file in the URL, so convert the response to json object.
    iss_json = response.json()
    # Make a copy of the json object as a dictionary, since that's all it seems to be.
    # Then we can work with the dictionary more easily, with dictionary functions.
    iss_dict = dict(iss_json)

    # Now we pick apart the nested dictionaries to get the positions we want.
    # We can see Longitude and Latitude are nested inside "iss_position" dictionary.
    # So let's get that one first. I forgot how to get keys from dictionaries, so I Googled.
    # https://www.geeksforgeeks.org/get-method-dictionaries-python/
    iss_pos = iss_dict.get("iss_position")

    # Then from that, grab the values for these keys, and make them floats so we can use them as numbers.
    # The strings need to be converted to floats because they're numbers like "32.9035".
    longitude = float(iss_pos.get("longitude"))
    latitude = float(iss_pos.get("latitude"))

    # Get the differences, ie how close the ISS is to being above OKC in degrees.
    # The absolute value just means the value regardless whether it's negative or positive. Thanks Google.
    # https://stackoverflow.com/questions/49180302/check-if-2-given-number-are-close-to-each-other-python
    iss_longitude_vicinity = abs(longitude - okc_long)
    iss_latitude_vicinity = abs(latitude - okc_lat)

    # Check and display the current distance.
    check_distance_smart()
    # Pause for 5 seconds before looping again.
    pause(5)