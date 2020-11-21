# This program reads text files in a given folder and (roughly) counts the words in each text file.

# ///////////////////// External Modules ////////////////////////////
import os
import pathlib
from time import sleep as pause


# ///////////////////// Classes / Methods ////////////////////////////
class WordCounter:

    def __init__(self):
        self.word_count = 0
        self.txt_file_content = ''
        self.words = []
        self.file_name = ''

    def folder_loop(self, folder_path):
        """
        START HERE:
        - This will check every file in the specified folder,
            and pass each text file over to the open_file and count_words
            methods.
        """

        # Just a simple for loop for every file in the given folder.
        for file in os.listdir(folder_path):
            # pass in the current file and the folder path too
            self.open_file(file, folder_path)
            self.count_words()

        # Once the above for loop is done, query to restart.
        pause(1)
        print(f"\nWanna check another folder? y/n\n")
        if input() != 'n':
            start()

    def open_file(self, file_name, folder_path):
        """
        Tries to open folder/file.txt for reading, with UTF-8 encoding.
        """
        try:
            with open(f"{folder_path}/{file_name}", 'r', encoding='UTF-8') as fileobject:
                # Store file's name for any use, in this case for printing in count_words().
                self.file_name = file_name
                # Here's where we read the text file object and label it as txt_file_content.
                self.txt_file_content = fileobject.read()

        except FileNotFoundError:
            print(f"We can't find {file_name} in this folder.")

        except UnicodeEncodeError:
            print(f"This file's encoding isn't in UTF-8! Put in some code here to offer some options."
                  f" I'm not smart enough to help here yet.")

    def count_words(self):
        """
        - Split the string of words into a list,
        - Count length of list as number of words,
        - Print it.
        - Should probably rewrite this with more specific regex since this will be not entirely accurate
           depending on superfluous text presence in the file.
        """
        self.words = self.txt_file_content.split()
        self.word_count = len(self.words)
        # The :, in {self.word_count} formats the string with commas for easier number reading.
        print(f"The file {self.file_name} has {self.word_count:,} words in it.")


# ///////////////////// Static Functions ////////////////////////////
def start():
    try:
        # Pass in the name of the folder where you saved the books to,
        #   preferably one that isn't in your root folder where WordCounter.py is.
        BookCount.folder_loop(input("Input the name of the folder containing your text files.\n"
                                    "This folder should be in your root path:\n"))

    except FileNotFoundError:
        print(f"Unable to locate a folder with that name. \n"
              f"Did you spell it correctly, and is your folder located in {pathlib.Path().absolute()}?\n"
              f"This will be the same directory where you saved this .py file.\n")
        pause(1)
        start()


# ///////////////////// Instancing ////////////////////////////
BookCount = WordCounter()

# ///////////////////// MAIN PROGRAM ////////////////////////////
# Pretty much just call start() function to press play and watch everything go to work.
start()
