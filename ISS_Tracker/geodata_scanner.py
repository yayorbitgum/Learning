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


# //////////////////////////////////////////// Variables ////////////////////////////////////////////
# Set acceptable degree difference here for returning coordinate matches.
# 1 degree of latitude/longitude = ~111 kilometers
tolerance = 2
# The data set paths, freshly converted to mappable hdf5.
folder_name = 'GeoLocationInfo/hdf5/'
national_file_path = f'{folder_name}NationalFile_20200501.hdf5'

global_files_list = [f'{folder_name}Countries_administrative_a.hdf5',   # 0
                     f'{folder_name}Countries_hydrographic_h.hdf5',     # 1
                     f'{folder_name}Countries_hypsographic_t.hdf5',     # 2
                     f'{folder_name}Countries_localities_l.hdf5',       # 3
                     f'{folder_name}Countries_populatedplaces_p.hdf5',  # 4 - Done.
                     f'{folder_name}Countries_spot_s.hdf5',             # 5
                     f'{folder_name}Countries_transportation_r.hdf5',   # 6
                     f'{folder_name}Countries_undersea_u.hdf5',         # 7
                     f'{folder_name}Countries_vegetation_v.hdf5'        # 8
                     ]


# //////////////////////////////////////////// Startup Logic ////////////////////////////////////////////
# When we launch the main program, open the hdf5 files and make them pandas dataframe objects.
print(f"Loading US geographical data..")

national_df = pd.read_hdf(national_file_path)
us_df_relevant = national_df[['FEATURE_NAME', 'STATE_ALPHA', 'PRIM_LAT_DEC', 'PRIM_LONG_DEC', 'ELEV_IN_M']]

print("US geographical data loaded!\n")
print(f"{us_df_relevant}\n")

print(f"Loading global geographical data..")
print(f"Loading populated places. This will take a moment..")

populated_df = pd.read_hdf(global_files_list[4])
populated_df_relevant = populated_df[['LAT', 'LONG', 'FULL_NAME_RO']]

print("Global populated locations loaded!\n")
print(f"{populated_df_relevant}\n")


# //////////////////////////////////////////// Functions ////////////////////////////////////////////
def scan_usa_df(iss_latitude, iss_longitude):
    """
    Take in ISS coordinates, and check for the closest locations in our US geographical dataframe.
    Returns 3 location values if not empty, otherwise returns None if it is empty.
    """

    # https://thispointer.com/python-pandas-select-rows-in-dataframe-by-conditions-on-multiple-columns/
    # So first we'll get a frame of the closest latitudes +- 0.02 degrees.
    closest_lat_df = us_df_relevant[
        (us_df_relevant['PRIM_LAT_DEC'] >= (iss_latitude - tolerance)) &
        (us_df_relevant['PRIM_LAT_DEC'] <= (iss_latitude + tolerance))
        ]

    # Then from those closest latitudes, we'll search for the closest longitude +- 0.02 degrees.
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


def scan_global_pop_df(iss_latitude, iss_longitude):
    """
    Take in ISS coordinates, and check for the closest locations in our
    global populated areas geographical dataframe.
    Returns 2 location values if not empty, otherwise returns None if it is empty.
    """

    # So first we'll get a frame of the closest latitudes +- 0.02 degrees.
    closest_lat_df = populated_df_relevant[
        (populated_df_relevant['LAT'] >= (iss_latitude - tolerance)) &
        (populated_df_relevant['LAT'] <= (iss_latitude + tolerance))
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
        #                                  [    middle index       ][  column ]
        result_pop_feature = result_df.iloc[int(len(result_df) / 2)]['FULL_NAME_RO']

        # Return the location name.
        return result_pop_feature

    # Otherwise if it is empty, return None.
    elif len(result_df) == 0:
        return None
