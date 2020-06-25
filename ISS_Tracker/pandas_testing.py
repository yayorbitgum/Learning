# This is me smashing my head into pandas trying to figure out how to search for
# the closest latitude and longitude in a dataframe, and return the info from that single row.

import pandas as pd

# The data set paths.
folder_name = 'GeoLocationInfo/hdf5/'
national_file_path = f'{folder_name}NationalFile_20200501.hdf5'

# Test values.
findme_lat = 35.384805
findme_long = -97.605344

# 0: ï»¿FEATURE_ID
# 1: FEATURE_NAME       <-
# 2: FEATURE_CLASS
# 3: STATE_ALPHA        <-
# 4: STATE_NUMERIC
# 5: COUNTY_NAME
# 6: COUNTY_NUMERIC
# 7: PRIMARY_LAT_DMS
# 8: PRIM_LONG_DMS
# 9: PRIM_LAT_DEC       <-
# 10: PRIM_LONG_DEC     <-
# 11: SOURCE_LAT_DMS
# 12: SOURCE_LONG_DMS
# 13: SOURCE_LAT_DEC
# 14: SOURCE_LONG_DEC
# 15: ELEV_IN_M         <-
# 16: ELEV_IN_FT
# 17: MAP_NAME
# 18: DATE_CREATED
# 19: DATE_EDITED

# This is how we open the hdf5 file and make it a pandas dataframe object.
national_df = pd.read_hdf(national_file_path)

# I can take a slice of the dataframe and make a new one, only including the four columns I want.
my_df = national_df[['FEATURE_NAME', 'STATE_ALPHA', 'PRIM_LAT_DEC', 'PRIM_LONG_DEC', 'ELEV_IN_M']]

# https://thispointer.com/python-pandas-select-rows-in-dataframe-by-conditions-on-multiple-columns/
# So first we'll get a frame of the closest latitudes +- 0.02 degrees.

closest_lat_df = my_df[
    (my_df['PRIM_LAT_DEC'] >= (findme_lat - 0.02)) &
    (my_df['PRIM_LAT_DEC'] <= (findme_lat + 0.02))
]

# Then from those closest latitudes, we'll search for the closest longitude +- 0.02 degrees.
# This should be our results of the closest locations with some room for imprecision.

result_df = closest_lat_df[
    (closest_lat_df['PRIM_LONG_DEC'] >= (findme_long - 0.02)) &
    (closest_lat_df['PRIM_LONG_DEC'] <= (findme_long + 0.02))
]

# We can grab a specific value in a cell with result_df.iloc[index]['column name']
# So the index is the length of result_df divided by 2, ie the average/median, converted to integer.

#                              [    middle index     ][  column name ]
result_feature = result_df.iloc[int(len(result_df)/2)]['FEATURE_NAME']

#                            [    middle index     ][ column name ]
result_state = result_df.iloc[int(len(result_df)/2)]['STATE_ALPHA']

#                                [    middle index     ][ column name ]
result_elevation = result_df.iloc[int(len(result_df)/2)]['ELEV_IN_M']

print(f"Our coordinates are closest to {result_feature} in {result_state}, at an elevation of {result_elevation:,} meters.")