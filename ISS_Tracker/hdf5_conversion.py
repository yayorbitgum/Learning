# I'll use this to convert our data files into hdf5 for mapping with vaex.
# https://www.christopherlovell.co.uk/blog/2016/04/27/h5py-intro.html
import h5py
from zipfile import ZipFile


def convert_data_to_hdf5(your_hf_filename, your_dataset_name, text_file):
    """
    I have to convert my data files to hdf5, to even use vaex to analyze my geolocation files.
    https://www.christopherlovell.co.uk/blog/2016/04/27/h5py-intro.html
    """

    # Here we initialize our files we're creating, in write mode. Now it's a file object with lots of cool methods.
    print(f"Opening {text_file} and creating new file {your_hf_filename}..")
    hf = h5py.File(your_hf_filename, 'w')

    # Now we make datasets in those file objects.
    # I ran into this error as well:
    # https://stackoverflow.com/questions/37121110/h5py-cannot-convert-element-0-to-hsize-t/37209236
    print(f"Creating data set as {your_dataset_name}..")
    # FIXME:
    #   This isn't working. Results in OSError: Can't write data (no appropriate function for conversion path)
    #   I'm probably running into this error because I don't know how to work with numpy and datasets yet,
    #   and I also don't know what the datasets I downloaded actually look like inside the text files.
    hf.create_dataset(your_dataset_name, data=text_file, dtype='int16')

    # And close the files, which will write the above changes to the disk.
    print("Saving changes to disk..")
    hf.close()


def open_file_and_convert(zip_name, file_name, choose_hf_filename, choose_dataset_name):
    """
    This will open the zip files, as well as pass in the file names,
    and the names you choose for output and naming your datasets in that file.
    :param zip_name: The zip file's path and name.
    :param file_name: The file inside the zip file we need, in this case the text files.
    :param choose_hf_filename: The name of the converted hf file you want to create.
    :param choose_dataset_name: The name of the dataset inside that hf file.
    """
    # open zip file.
    with ZipFile(zip_name) as myzip:
        # open the text file inside that zip file.
        with myzip.open(file_name) as text_file:
            # Convert that text file to hdf5, and pass in our names we choose too.
            convert_data_to_hdf5(choose_hf_filename, choose_dataset_name, text_file)


# //////////////////// Program ////////////////////////
# Now we pass in all our info.
# National File (all US map info):
open_file_and_convert('GeoLocationInfo/NationalFile.zip',
                      'NationalFile_20200501.txt',
                      'GeoLocationInfo/NationalFile.h5',
                      'national_dataset')

# Foreign File (all global map info outside the US):
open_file_and_convert('GeoLocationInfo/ForeignFile.zip',
                      'Countries.txt',
                      'GeoLocationInfo/ForeignFile.h5',
                      'foreign_dataset')
