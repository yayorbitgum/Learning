# Here I'm doing my best to write a script that converts these data text csv files to hdf5 files.
#
# For now this only works with the files I needed to convert specifically for the ISS project.
# In the future, especially as I learn databases, data types, and pandas more,
# I think I could modify this to accept any data file and output hdf5 as a result.

# ///////////////////////////// Imports /////////////////////////////
import os
import pandas as pd
# While I'm not using "tables" module here, pandas is dependent on it for what we're doing
#   as I got an error before.
#       "pip install tables"

# Pandas uses numexpr. I can set my max threads for doing logic.
# I found this out through warnings it was giving me on initial tests.
# Ryzen 5 3600 has 6 cores, 12 threads, so let's set max to 12 instead of the default 8.
# If I were to release this for others, I'm sure I figure out a way to set this automatically
# based on current user's processor.
os.environ['NUMEXPR_MAX_THREADS'] = '12'


# ///////////////////////////// Variables /////////////////////////////
# Set our file path names.

us_file_name = 'GeoLocationInfo/NationalFile_20200501.txt'
# Header Results for NationalFile_20200501.txt
# 0: ï»¿FEATURE_ID
# 1: FEATURE_NAME       <- Usable Name for City or Land Feature.
# 2: FEATURE_CLASS
# 3: STATE_ALPHA        <- State Abbreviation.
# 4: STATE_NUMERIC
# 5: COUNTY_NAME
# 6: COUNTY_NUMERIC
# 7: PRIMARY_LAT_DMS
# 8: PRIM_LONG_DMS
# 9: PRIM_LAT_DEC       <- Latitude using decimals.
# 10: PRIM_LONG_DEC     <- Longitude using decimals.
# 11: SOURCE_LAT_DMS
# 12: SOURCE_LONG_DMS
# 13: SOURCE_LAT_DEC
# 14: SOURCE_LONG_DEC
# 15: ELEV_IN_M
# 16: ELEV_IN_FT
# 17: MAP_NAME
# 18: DATE_CREATED
# 19: DATE_EDITED

global_files_list = ['Countries_administrative_a.txt',
                     'Countries_hydrographic_h.txt',
                     'Countries_hypsographic_t.txt',
                     'Countries_localities_l.txt',
                     'Countries_populatedplaces_p.txt',
                     'Countries_spot_s.txt',
                     'Countries_transportation_r.txt',
                     'Countries_undersea_u.txt',
                     'Countries_vegetation_v.txt',
                     ]
# All global text data sets have the same header, so we can use this for all those Countries files.
# Index: 0. Column Header: RC.
# Index: 1. Column Header: UFI.
# Index: 2. Column Header: UNI.
# Index: 3. Column Header: LAT.                 <- Latitude!
# Index: 4. Column Header: LONG.                <- Longitude!
# Index: 5. Column Header: DMS_LAT.
# Index: 6. Column Header: DMS_LONG.
# Index: 7. Column Header: MGRS.
# Index: 8. Column Header: JOG.
# Index: 9. Column Header: FC.
# Index: 10. Column Header: DSG.
# Index: 11. Column Header: PC.
# Index: 12. Column Header: CC1.
# Index: 13. Column Header: ADM1.               ! Contains mixed types.
# Index: 14. Column Header: POP.
# Index: 15. Column Header: ELEV.
# Index: 16. Column Header: CC2.                ! Contains mixed types.
# Index: 17. Column Header: NT.
# Index: 18. Column Header: LC.                 ! Contains mixed types.
# Index: 19. Column Header: SHORT_FORM.         ! Contains mixed types.
# Index: 20. Column Header: GENERIC.            <- Usable Name. Also mixed types.
# Index: 21. Column Header: SORT_NAME_RO.
# Index: 22. Column Header: FULL_NAME_RO.       <- Usable Name.
# Index: 23. Column Header: FULL_NAME_ND_RO.    <- Usable Name.
# Index: 24. Column Header: SORT_NAME_RG.
# Index: 25. Column Header: FULL_NAME_RG.
# Index: 26. Column Header: FULL_NAME_ND_RG.
# Index: 27. Column Header: NOTE.               ! Contains mixed types.
# Index: 28. Column Header: MODIFY_DATE.
# Index: 29. Column Header: DISPLAY.
# Index: 30. Column Header: NAME_RANK.
# Index: 31. Column Header: NAME_LINK.
# Index: 32. Column Header: TRANSL_CD.          ! Contains mixed types.
# Index: 33. Column Header: NM_MODIFY_DATE.
# Index: 34. Column Header: F_EFCTV_DT.         ! Contains mixed types.
# Index: 35. Column Header: F_TERM_DT.          ! Contains mixed types.


# ///////////////////////////// Functions /////////////////////////////
# Our data is in text files, in csv format, with different seperators/delimiters.
# National US file is separated by | and the international files are separated by \t.
# This is all to work towards having data that can be worked with quickly, memory mappable.


def national_csv_to_hdf5():
    """Convert our national text file to hdf5 format, and save it to disk."""
    separator = '|'
    output_name = 'GeoLocationInfo/hdf5/NationalFile_20200501.hdf5'

    # Read text file into dataframe object.
    print(f"Reading {us_file_name} as csv with pandas..")
    us_df = pd.read_csv(us_file_name,
                        delimiter=separator,
                        # I had to set all of this manually after performance warnings.
                        # Everything was an object type, more or less.
                        dtype={'FEATURE_NAME': str,
                               'FEATURE_CLASS': str,
                               'STATE_ALPHA': str,
                               'STATE_NUMERIC': str,
                               'COUNTY_NAME': str,
                               'COUNTY_NUMERIC': str,
                               'PRIMARY_LAT_DMS': str,
                               'PRIM_LONG_DMS': str,
                               'PRIM_LAT_DEC': float,
                               'PRIM_LONG_DEC': float,
                               'SOURCE_LAT_DMS': str,
                               'SOURCE_LONG_DMS': str,
                               'SOURCE_LAT_DEC': float,
                               'SOURCE_LONG_DEC': float,
                               'ELEV_IN_M': float,
                               'ELEV_IN_FT': float,
                               'MAP_NAME': str,
                               'DATE_CREATED': str,
                               'DATE_EDITED': str}
                        )

    # Save to HDF5 file in the hdf5 folder.
    pd.DataFrame.to_hdf(us_df,
                        path_or_buf=output_name,
                        mode='w',
                        format='fixed',
                        key='nat',
                        )

    # Clear this object from memory after conversion is done!
    print("Clearing memory..")
    del us_df
    # Let us know we're finished!
    print("All done!\n")


def global_csv_to_hdf5():
    """Convert our global text files to hdf5 format, and save it to disk."""
    separator = '\t'
    output_folder_path = 'GeoLocationInfo/hdf5'
    current_folder = 'GeoLocationInfo'
    count = len(global_files_list)
    counter = 0

    # For each file in our global text files list:
    for index, current_file in enumerate(global_files_list):
        # Increment the count for log.
        counter += 1
        # this will make sure each save has a unique name.
        path_name = f"{output_folder_path}/{current_file.rstrip('.txt')}.hdf5"

        # Read the current file in the list.
        print(f"{counter} of {count}: Reading {current_file} as csv with pandas..")
        # Some of these data files have mixed types in their columns as we see above in the notes,
        # so we'll make them explicitly one type.
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.errors.DtypeWarning.html
        current_df = pd.read_csv(f"{current_folder}/{current_file}",
                                 delimiter=separator,
                                 dtype={'ADM1': str,
                                        'CC2': str,
                                        'NOTE': str,
                                        'TRANSL_CD': str,
                                        'F_EFCTV_DT': str,
                                        'F_TERM_DT': str,
                                        'SHORT_FORM': str,
                                        'LC': str,
                                        'GENERIC': str
                                        }
                                 )

        # Save to HDF5 file in the hdf5 folder.
        print(f"{counter} of {count}: Converting to hdf5 format and saving as {path_name}..")
        pd.DataFrame.to_hdf(current_df,
                            path_or_buf=path_name,
                            mode='w',
                            format='fixed',
                            key='earth')

        # Clear this object from memory after conversion is done.
        print(f"{counter} of {count}: Clearing dataframe from memory..")
        del current_df

        # Let us know we're finished.
        if counter != count:
            print(f"{counter} of {count}: All done! Starting next file..\n")
        else:
            print(f"{counter} of {count}: All done! Shutting down program.\n"
                  f"Check your folder '{output_folder_path}'for outputs!")


# ///////////////////////////// Program /////////////////////////////
national_csv_to_hdf5()
global_csv_to_hdf5()
