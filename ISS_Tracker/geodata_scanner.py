"""
This will get the name of the current location based on ISS coordinates.

I found some data for locations, which should allow me to tie coordinates to real location names and
    other things.
For US locations:
    https://www.usgs.gov/core-science-systems/ngp/board-on-geographic-names/download-gnis-data
For foreign locations:
    https://geonames.nga.mil/gns/html/namefiles.html

These files are sort of big (2-3gb), so I worked on learning to convert them to hdf5 for memory mapping,
    so that this module called Vaex can read them nearly instantly. But I couldn't get vaex to export hdf5.
    It provided no error when exporting, simply hangs and does not proceed after a certain point.
    So I did pandas hdf5 exports instead, and since Vaex can't read pandas-made hdf5, I'll just
    use pandas for this task and we'll try Vaex in the future.

I found out about Vaex by coming across this article.
https://towardsdatascience.com/how-to-analyse-100s-of-gbs-of-data-on-your-laptop-with-python-f83363dda94
"""


# //////////////////////////////////////////// Imports ////////////////////////////////////////////
import pandas as pd
import re
import os


# //////////////////////////////////////////// Variables and File Structure ////////////////////////////////////////////
# Set acceptable degree difference here for returning coordinate matches.
# 1.0 degree of latitude/longitude = ~111 kilometers
tolerance = 0.5
# The data set paths for our hdf5 files.
folder_name = 'GeoLocationInfo/hdf5/'
# This regex should help us load any NationalFile version that we might use.
# https://regex101.com/
national_regex = re.compile('(NationalFile)(_)?(\d*)?(\.hdf5)')
# Now we locate the national file.
for findme in os.listdir('GeoLocationInfo/hdf5'):
    if national_regex.match(findme):
        national_file_path = f'{folder_name}{findme}'

global_files_list = [f'{folder_name}Countries_administrative_a.hdf5',   # 0
                     f'{folder_name}Countries_hydrographic_h.hdf5',     # 1
                     f'{folder_name}Countries_hypsographic_.hdf5',      # 2
                     f'{folder_name}Countries_localities_l.hdf5',       # 3
                     f'{folder_name}Countries_populatedplaces_p.hdf5',  # 4
                     f'{folder_name}Countries_spot_s.hdf5',             # 5
                     f'{folder_name}Countries_transportation_r.hdf5',   # 6
                     f'{folder_name}Countries_undersea_u.hdf5',         # 7
                     f'{folder_name}Countries_vegetation_v.hdf5'        # 8
                     ]


# //////////////////////////////////////////// Classes/Methods ////////////////////////////////////////////
class LocationLove:
    def __init__(self, iss_latitude, iss_longitude):
        self.iss_latitude = iss_latitude
        self.iss_longitude = iss_longitude
        self.us_df = None
        self.global_df = None

    def startup_load(self):
        """Loads all hdf5 files into dataframes to be used for searching."""
        global_df_list = []
        count = 0
        print(f"Loading US geographical data..")

        # Read us-based data file.
        national_df = pd.read_hdf(national_file_path)
        # Only grab the columns we care about (I should probably save this as another file and skip this step).
        self.us_df = national_df[['FEATURE_NAME',
                                  'STATE_ALPHA',
                                  'PRIM_LAT_DEC',
                                  'PRIM_LONG_DEC',
                                  'ELEV_IN_M']]
        print("US geographical data loaded!\n")
        # Show a sample to confirm.
        print(f"{self.us_df}\n")

        # We'll loop through our list of global files, add each dataframe to a list, then
        # concatenate those dataframes together with pd.concat.
        print(f"Loading all global geographical data. This will take a moment..")
        for index, file in enumerate(global_files_list):
            count += 1
            # Show current step, file and how many more to go.
            print(f"{count} of {len(global_files_list)}: Reading {file.lstrip(folder_name)}..")
            # Read the current file into dataframe.
            this_full_df = pd.read_hdf(file)
            # Grab the columns we want. Most of the other data is empty or useless unfortunately.
            this_df = this_full_df[['LAT', 'LONG', 'FULL_NAME_ND_RG']]
            global_df_list.append(this_df)

        # https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
        print("Merging global dataframes..\n")
        # If I set the keys, I can actually locate (df.loc[]) based on the original data categories too.
        self.global_df = pd.concat(global_df_list,
                                   ignore_index=True,
                                   keys=['administrative',
                                         'hydrographic',
                                         'hypsographic',
                                         'localities',
                                         'populated places',
                                         'spot locations',
                                         'transportation',
                                         'undersea',
                                         'vegetation'])

        # Show a sample to confirm.
        print(f"{self.global_df}\n")
        print("Complete!\n")

    def scan_usa_df(self, iss_latitude, iss_longitude):
        """
        Take in ISS coordinates, and check for the closest locations in our US geographical dataframe.
        Returns 3 location values if not empty, otherwise returns None if it is empty.
        """

        # https://thispointer.com/python-pandas-select-rows-in-dataframe-by-conditions-on-multiple-columns/
        # So first we'll get a frame of the closest latitudes +- some degrees of tolerance we set earlier.
        closest_lat_df = self.us_df[
            (self.us_df['PRIM_LAT_DEC'] >= (iss_latitude - tolerance)) &
            (self.us_df['PRIM_LAT_DEC'] <= (iss_latitude + tolerance))
            ]

        # Then from those closest latitudes, we'll search for the closest longitude +- some degrees.
        # This should be our results of the closest locations with some room for imprecision.
        result_df = closest_lat_df[
            (closest_lat_df['PRIM_LONG_DEC'] >= (iss_longitude - tolerance)) &
            (closest_lat_df['PRIM_LONG_DEC'] <= (iss_longitude + tolerance))
            ]

        # If the result isn't nothing:
        if len(result_df) != 0:
            # We can grab a specific value in a cell with result_df.iloc[index]['column name']
            # So the index is the length of result_df divided by 2, ie the average/median, converted to integer.
            #                                 [    middle index       ][  column name ]
            result_us_feature = result_df.iloc[int(len(result_df) / 2)]['FEATURE_NAME']
            result_us_state = result_df.iloc[int(len(result_df) / 2)]['STATE_ALPHA']
            result_us_elevation = result_df.iloc[int(len(result_df) / 2)]['ELEV_IN_M']

            # Return all three results as a list we can pick apart later.
            return [result_us_feature, result_us_state, result_us_elevation]

        # Otherwise if it is, return None.
        elif len(result_df) == 0:
            return None

    def scan_global_pop_df(self, iss_latitude, iss_longitude):
        """
        Take in ISS coordinates, and check for the closest locations in our
        global populated areas geographical dataframe.
        Returns 2 location values if not empty, otherwise returns None if it is empty.
        """

        # So first we'll get a frame of the closest latitudes +- 0.02 degrees.
        closest_lat_df = self.global_df[
            (self.global_df['LAT'] >= (iss_latitude - tolerance)) &
            (self.global_df['LAT'] <= (iss_latitude + tolerance))
            ]

        # Then from those closest latitudes, we'll search for the closest longitude +- 0.02 degrees.
        # This should be our results of the closest locations with some room for imprecision.
        result_df = closest_lat_df[
            (closest_lat_df['LONG'] >= (iss_longitude - tolerance)) &
            (closest_lat_df['LONG'] <= (iss_longitude + tolerance))
            ]

        # If the result isn't nothing:
        if len(result_df) != 0:
            # We can grab a specific value in a cell with result_df.iloc[index]['column name']
            # So the index is the length of result_df divided by 2, ie the average/median, converted to integer.
            #                                  [    middle index       ][     column      ]
            result_pop_feature = result_df.iloc[int(len(result_df) / 2)]['FULL_NAME_ND_RG']

            # Return the location name.
            return result_pop_feature

        # Otherwise if it is empty, return None.
        elif len(result_df) == 0:
            return None
