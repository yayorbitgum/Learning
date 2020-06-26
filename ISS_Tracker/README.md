# ISS Location Tracker

Keeps track of current International Space Station location using API from http://api.open-notify.org/, checks to see if it's above your input coordinates or nearby, and displays the current distance away from the center of your sky. Also displays the name of geographical locations the ISS is flying over.

# Installation instructions (if you want to try it yourself):
- Requires Python 3+, of course.
- Make sure your directory matches this folder, with ISS_Tracker as the root folder.
- Install the modules listed in requirements.txt.
    - pip install -r requirements.txt
- Download two database csv text files (around 655mb zipped, ~3gb unzipped) and unzip them into the GeoLocationInfo folder, as shown in here on github. These are required for showing current geographical locations that the ISS is flying directly above within a certain tolerance of degrees/kilometers.
    - US locations (National File (all features in one file)): 
        - https://www.usgs.gov/core-science-systems/ngp/board-on-geographic-names/download-gnis-data
    - Global locations (Entire country files dataset separated by feature class): 
        - https://geonames.nga.mil/gns/html/namefiles.html
- Use the hdf5_converter.py script I made to convert the unzipped text files to hdf5 format for fast reading.
    - You may need to make sure a folder named "hdf5" is inside the GeoLocationInfo folder.
- Run ISS_Location_Tracker.py!

# TODO:

- Add easier user input.
    - Ability to enter any location text.
    - Ability to enter both coordinates at the same time, or copy/paste from common sources and formats.
- Make some coordinate ranges that correspond to giant empty oceans we can check, so we know at least which oceans the ISS is flying over when it's too far away for any other results.
- Make an actual interface, so the changing info is easier to take in than lines in the console. Web-based interface would be nice.
    - Add ability to stop program at any time.
    - Add ability to adjust update rate at any time.
    - Add ability to adjust coordinate match tolerance range at any time.
- Plotting of ISS course on a world map (would be interesting to see it line up with NASA data).
