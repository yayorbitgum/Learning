"""
This will get the name of the current location based on ISS coordinates.
I found some data for locations, which should allow me to tie coordinates to real location names and
    other things.
For US locations:
    https://www.usgs.gov/core-science-systems/ngp/board-on-geographic-names/download-gnis-data
For foreign locations:
    https://geonames.nga.mil/gns/html/namefiles.html
These files are sort of big (2-3gb), so I need to learn how to work with them.
They aren't so big that they won't fit in RAM, but at the same time I'm sure performance won't be great
    unless I figure out the tools listed in this page:
    https://towardsdatascience.com/how-to-analyse-100s-of-gbs-of-data-on-your-laptop-with-python-f83363dda94
Either way, I also need to learn pandas..
    https://www.learndatasci.com/tutorials/python-pandas-tutorial-complete-introduction-for-beginners/
"""


def get_data_details(reader, iss_latitude, iss_longitude):
    # Checking to see what all the headers are, laid out neatly with their index visible.
    # header_row = next(reader)
    # for index, column_header in enumerate(header_row):
    #    print(f"{index}: {column_header}")
    #
    # Header Results for NationalFile_20200501.txt
    # 0: ï»¿FEATURE_ID
    # 1: FEATURE_NAME
    # 2: FEATURE_CLASS
    # 3: STATE_ALPHA
    # 4: STATE_NUMERIC
    # 5: COUNTY_NAME
    # 6: COUNTY_NUMERIC
    # 7: PRIMARY_LAT_DMS
    # 8: PRIM_LONG_DMS
    # 9: PRIM_LAT_DEC
    # 10: PRIM_LONG_DEC
    # 11: SOURCE_LAT_DMS
    # 12: SOURCE_LONG_DMS
    # 13: SOURCE_LAT_DEC
    # 14: SOURCE_LONG_DEC
    # 15: ELEV_IN_M
    # 16: ELEV_IN_FT
    # 17: MAP_NAME
    # 18: DATE_CREATED
    # 19: DATE_EDITED

    # Get Feature Name[1], State Name[3], and the coordinates in decimal degrees [9 and 10].
    # For each row in the csv reader object that opened the file:
    for index, row in enumerate(reader):
        # We need to make sure we aren't grabbing the header row, because then row values 9 and 10 aren't numbers.
        if index != 0:
            # Grab each thing from each column. Convert degrees to floats so we can do math with them.
            feature_name = row[1]
            state_name = row[3]
            location_latitude = float(row[9])
            location_longitude = float(row[10])

            # See if we're close to this row's location, with an absolute value so it's never negative.
            # One degree of latitude or longitude is about 111km. So maybe 0.2 degrees is around 20km.
            if abs(iss_latitude - location_latitude) < 0.2 and abs(iss_longitude - location_longitude) < 0.2:
                # Then return the name of this location the ISS is above!
                return f"{feature_name} in {state_name}"