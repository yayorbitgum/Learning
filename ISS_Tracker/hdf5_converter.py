# Here I'm doing my best to write a script that converts these data text csv files to hdf5 files.
#
# For now this only works with the files I needed to convert specifically for the ISS project.
# In the future, especially as I learn databases, data types, and pandas more,
# I think I could modify this to accept any data file and output hdf5 as a result.

# ///////////////////////////// Imports /////////////////////////////

import os
import pandas as pd
import re
# While I'm not using "tables" module, pandas is dependent on it for what we're doing
#   as I got an error before. I added it to requirements.txt.

# Pandas uses numexpr. I can set my max threads for doing logic.
# I found this out through warnings it was giving me on initial tests.
# Ryzen 5 3600 has 6 cores, 12 threads, so let's set max to 12 instead of the default 8.
# If I were to release this for others, I'm sure I figure out a way to set this automatically
# based on current user's processor.
os.environ['NUMEXPR_MAX_THREADS'] = '12'


# ///////////////////////////// Header Reference /////////////////////////////

# Header info for National text file.
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
# Index: 24. Column Header: SORT_NAME_RG.       <- Usable Name.
# Index: 25. Column Header: FULL_NAME_RG.       <- Usable Name.
# Index: 26. Column Header: FULL_NAME_ND_RG.    <- Usable Name.
# Index: 27. Column Header: NOTE.               ! Contains mixed types.
# Index: 28. Column Header: MODIFY_DATE.
# Index: 29. Column Header: DISPLAY.            <- Best name?
# Index: 30. Column Header: NAME_RANK.
# Index: 31. Column Header: NAME_LINK.
# Index: 32. Column Header: TRANSL_CD.          ! Contains mixed types.
# Index: 33. Column Header: NM_MODIFY_DATE.
# Index: 34. Column Header: F_EFCTV_DT.         ! Contains mixed types.
# Index: 35. Column Header: F_TERM_DT.          ! Contains mixed types.


# ///////////////////////////// Variables /////////////////////////////

# Set our file path names.
folder_name = 'GeoLocationInfo'
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


# ///////////////////////////// Functions /////////////////////////////

# Our data is in text files, in csv format, with different separators/delimiters.
# National US file is separated by | and the international files are separated by \t.
# This is all to work towards having data that can be worked with quickly, memory mappable.

def find_national_file():
    """
    Since the national file has a different name depending on the date they updated it on
    the website we downloaded it from, I need to make sure we catch whatever version the
    person running this program ends up downloading.
    """
    # This regex should help us load any NationalFile version that we might use.
    # https://regex101.com/
    national_regex = re.compile('((NationalFile)(_)?(\d*)?(\.txt))')
    # Now we locate the national text file.
    print("Searching for national file..")
    for file in os.listdir(folder_name):
        # Skip subfolders to avoid errors.
        # https://stackoverflow.com/questions/22207936/python-how-to-find-files-and-skip-directories-in-os-listdir
        path = os.path.join(folder_name, file)
        if os.path.isdir(path):
            print(f"Skipping {path}..")
            continue

        # If current file matches our regex:
        # https://stackoverflow.com/questions/39293968/python-how-do-i-search-directories-and-find-files-that-match-regex
        elif national_regex.match(file):
            print(f"Found {file}!")
            # Return it.
            return file


def national_csv_to_hdf5():
    """Convert our national text file to hdf5 format, and save it to disk."""
    us_file_name = find_national_file()
    separator = '|'
    output_name = f'{folder_name}/hdf5/{us_file_name.rstrip(".txt")}.hdf5'

    # Read text file into dataframe object.
    print(f"Reading {us_file_name} with pandas..")
    us_df = pd.read_csv(f'{folder_name}/{us_file_name}',
                        delimiter=separator,
                        )
    print("\nComplete!")

    # An attempt to resolve performance warnings I was getting before.
    # https://stackoverflow.com/questions/22998859/hdfstore-with-string-columns-gives-issues
    columns = ['FEATURE_NAME', 'FEATURE_CLASS', 'STATE_ALPHA', 'STATE_NUMERIC', 'COUNTY_NAME',
               'COUNTY_NUMERIC', 'PRIMARY_LAT_DMS', 'PRIM_LONG_DMS', 'SOURCE_LAT_DMS', 'SOURCE_LONG_DMS',
               'MAP_NAME', 'DATE_CREATED', 'DATE_EDITED']
    # We locate all our columns listed, then apply string type to every column.
    # Now they'll be fast strings instead of slow objects.
    us_df.loc[:, columns] = us_df[columns].applymap(str)

    # Now we this save this dataframe to HDF5 file in the hdf5 folder.
    print(f"Converting {us_file_name} to hdf5 format...")
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
        print(f"{counter} of {count}: Reading {current_file} with pandas..")
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

        # An attempt to resolve performance warnings I was getting before.
        # https://stackoverflow.com/questions/22998859/hdfstore-with-string-columns-gives-issues
        columns = ['MGRS', 'JOG', 'FC', 'DSG', 'CC1', 'ADM1', 'CC2', 'NT', 'LC', 'SHORT_FORM', 'GENERIC',
                   'SORT_NAME_RO', 'FULL_NAME_RO', 'FULL_NAME_ND_RO', 'SORT_NAME_RG', 'FULL_NAME_RG',
                   'FULL_NAME_ND_RG', 'NOTE', 'MODIFY_DATE', 'DISPLAY', 'TRANSL_CD', 'NM_MODIFY_DATE',
                   'F_EFCTV_DT', 'F_TERM_DT', 'DMS_LAT', 'DMS_LONG']
        # We locate all our columns listed, then apply string type to every column.
        # Now they'll be fast strings instead of slow objects.
        current_df.loc[:, columns] = current_df[columns].applymap(str)

        # Save this dataframe to HDF5 file in the hdf5 folder.
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
