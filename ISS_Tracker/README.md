# ISS Location Tracker

Keeps track of current International Space Station location using API from http://api.open-notify.org/, checks to see if it's above me in OKC or nearby, and displays the current distance away from the center of my sky. Also displays information about geographical locations the ISS is flying over, if they're in the US or in populated areas on the globe.

WIP features:

- Check current ISS coordinates and showing if it's flying over any and all global features, including ocean and underwater locations.. Assuming they're in these databases.
- Input current location to check distance from wherever, not just OKC.
- Interface, visual map representation.
- Plotting of ISS course (would be interesting to see it line up with NASA data).

# Installation instructions (if you want to try it yourself):
-1: Install the modules listed in requirements.txt.
  - pip install -r requirements.txt
-2: Download two database csv text files (around 655mb zipped, ~3gb unzipped) and unzip them into the GeoLocationInfo folder, as shown in here on github. These are required for showing current geographical locations that the ISS is flying directly above within a certain tolerance of degrees/kilometers.
  - US locations (National File): https://www.usgs.gov/core-science-systems/ngp/board-on-geographic-names/download-gnis-data
  - Global locations (separated by feature class): https://geonames.nga.mil/gns/html/namefiles.html
-3: Use the hdf5_converter.py script I made to convert the unzipped text files to hdf5 format for fast reading.
  - You may need to make sure a folder named "hdf5" is inside the GeoLocationInfo folder, but it might create it for you.
  - You can also convert these files yourself if you'd like to! It was done with pandas, with errors, so you may be able to do a much better conversion than I did.
    - The National File uses | as a delimiter.
    - The global files use \t as a delimiter.
-4: Run ISS_Location_Tracker.py!
