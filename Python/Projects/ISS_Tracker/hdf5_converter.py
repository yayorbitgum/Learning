# Here I'm doing my best to write a script that converts these data text csv files to hdf5 files.
#
# For now this only works with the files I needed to convert specifically for the ISS project.
# In the future I think I could modify this to accept any data file and output hdf5 as a result.

# Imports ----------------------------------------------------------------------
# TODO: Need to resolve 'tables' dependencies and resulting HDF5 errors.
import os
import pandas as pd
import re
import multiprocessing
# Importing lists from another file just for keeping code looking clean.
import db_headers

# Variables --------------------------------------------------------------------
# Pandas uses numexpr, and with it I can set max threads for doing logic, for max performance.
os.environ['NUMEXPR_MAX_THREADS'] = str(multiprocessing.cpu_count())
folder_name = 'GeoLocationInfo'
global_files_list = ['Countries_administrative_a.txt',
                     'Countries_hydrographic_h.txt',
                     'Countries_hypsographic_t.txt',
                     'Countries_localities_l.txt',
                     'Countries_populatedplaces_p.txt',
                     'Countries_spot_s.txt',
                     'Countries_transportation_r.txt',
                     'Countries_undersea_u.txt',
                     'Countries_vegetation_v.txt',]


# Functions --------------------------------------------------------------------
# Our data is in text files, in csv format, with different separators/delimiters.
# National US file is separated by | and the international files are separated by \t.
def find_national_file():
    """
    The national file has a different name depending on the date they updated it on
    the website we downloaded it from, so this function will use regex to find
    the national database file regardless of the exact date in the name.
    """
    national_regex = re.compile('((NationalFile)(_)?(\d*)?(\.txt))')
    print("Searching for national file..")
    for file in os.listdir(folder_name):
        # Skip subfolders to avoid errors.
        path = os.path.join(folder_name, file)
        if os.path.isdir(path):
            print(f"Skipping {path}..")
            continue

        elif national_regex.match(file):
            print(f"Found {file}!")
            return file


def national_csv_to_hdf5():
    """Convert our national text file to hdf5 format and save it."""
    us_file_name = find_national_file()
    sep = '|'
    output_name = f'{folder_name}/hdf5/{us_file_name.rstrip(".txt")}.hdf5'

    print(f"Reading {us_file_name} with pandas..")
    us_df = pd.read_csv(f'{folder_name}/{us_file_name}', delimiter=sep)

    # https://stackoverflow.com/questions/22998859/hdfstore-with-string-columns-gives-issues
    # Converting mixed objects to consistent string type so it's much faster.
    columns = db_headers.national_columns
    us_df.loc[:, columns] = us_df[columns].applymap(str)

    print(f"Converting {us_file_name} to hdf5 format...")
    pd.DataFrame.to_hdf(us_df, path_or_buf=output_name, mode='w', format='fixed', key='nat')
    print("Clearing memory..")
    del us_df


def global_csv_to_hdf5():
    """Convert our global text files to hdf5 format and save it."""
    sep = '\t'
    output_folder_path = 'GeoLocationInfo/hdf5'
    current_folder = 'GeoLocationInfo'
    count = len(global_files_list)
    counter = 0

    # --------------------------------------------------------------------------
    # Self reminder: For each file in our global text files list:
    for index, current_file in enumerate(global_files_list):
        # Make sure each save has a unique name.
        path_name = f"{output_folder_path}/{current_file.rstrip('.txt')}.hdf5"
        print(f"{counter} of {count}: Reading {current_file} with pandas..")

        # Converting all mixed data types to string for performance. -----------
        current_df = pd.read_csv(f"{current_folder}/{current_file}",
                                 delimiter=sep,
                                 dtype={'ADM1': str,
                                        'CC2': str,
                                        'NOTE': str,
                                        'TRANSL_CD': str,
                                        'F_EFCTV_DT': str,
                                        'F_TERM_DT': str,
                                        'SHORT_FORM': str,
                                        'LC': str,
                                        'GENERIC': str})

        columns = db_headers.global_columns
        current_df.loc[:, columns] = current_df[columns].applymap(str)

        print(f"{counter} of {count}: Converting to hdf5 format and saving as {path_name}..")
        pd.DataFrame.to_hdf(current_df,
                            path_or_buf=path_name,
                            mode='w',
                            format='fixed',
                            key='earth')

        print(f"{counter} of {count}: Clearing dataframe from memory..")
        del current_df

        if counter != count:
            print(f"{counter} of {count}: Starting next file..\n")
        else:
            print(f"{counter} of {count}: Shutting down program.\n"
                  f"Check '{output_folder_path}'for outputs.")


# ------------------------------------------------------------------------------
national_csv_to_hdf5()
global_csv_to_hdf5()
