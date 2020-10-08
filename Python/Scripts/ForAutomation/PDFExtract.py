# This will extract text, images, and text inside those images from a provided
#   PDF file.
#
# Reference info:
# AtBS Chapter 15.
# https://pypi.org/project/pytesseract/
# https://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python
# https://pymupdf.readthedocs.io/en/latest/faq.html#how-to-extract-images-pdf-documents
# https://stackoverflow.com/questions/56494070/how-to-use-pdfminer-six-with-python-3/56530666#56530666


# Imports ----------------------------------------------------------------------
# TODO: Figure out why PyPDF4 text extract is a mess or find alternative.
import pdfminer3
import PyPDF4
import pytesseract
from PIL import Image
# Fitz however is working perfectly for images extracts.
import fitz
import os
import logging
from datetime import datetime


# Timestamp for the log files. -------------------------------------------------
# Timestamp formatting is too messy to be used for file name:
#   (2020-09-19 18:00:50.263646), so I'll make my own.
# I'll also add zeros to ensure each slot is at least 2 digits long so that
#   sorting by file name works.
now = datetime.now()
timestamp = datetime.timestamp(now)
time_format = datetime.fromtimestamp(timestamp)


def add_a_zero(number):
    if len(str(number)) < 2:
        number = f"0{number}"
        return number
    else:
        return number


year   = time_format.year
month  = add_a_zero(time_format.month)
day    = add_a_zero(time_format.day)
hour   = add_a_zero(time_format.hour)
minute = add_a_zero(time_format.minute)
second = add_a_zero(time_format.second)

time = f"{year}-{month}-{day} {hour}.{minute}.{second}"


# Logging ----------------------------------------------------------------------
# The console spam is way too fast for me to review!
# https://stackoverflow.com/a/17682520/13627106
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()
# Shadowing print here is intentional so all prints are replaced with logging.
print = logger.info
log_folder = f'{os.getcwd()}/PDFExtract Logs'

try:
    os.makedirs(log_folder)
except FileExistsError:
    pass

logger.addHandler(logging.FileHandler(
    f'{log_folder}/PDFExtract log {time}.txt',
    'w'))


# Classes ----------------------------------------------------------------------
class PDFAnalyzer:
    # This class can extract text, images, and text from images in PDFs.
    # directory: The folder the PDF is located in.
    # file_name: the PDF file name (including .pdf).
    # page_number (optional): Specify specific page number.

    def __init__(self, directory, file_name, *page_number):
        self.file_name = file_name
        self.directory = directory
        self.pdf_full_path = f"{directory}/{file_name}"
        self.page_number = page_number
        self.page_amt = 0
        # Logging file.

    def image_extract(self):
        # Extract images from given PDF file, and save as PNGs in given folder.

        pdf_doc = fitz.open(self.pdf_full_path)
        # New folder for extracted images.
        img_folder_path = f"{self.directory}/extracted images"
        try:
            os.makedirs(img_folder_path)
        except FileExistsError:
            pass

        # Check each page for images, then grab xref and pixel info. -----------
        # xref is a cross reference number stored in PDF to locate objects.
        for page in range(len(pdf_doc)):
            try:
                for img in pdf_doc.getPageImageList(page):
                    print(f"Found {img[-1]} image on page {page}.")
                    xref = img[0]
                    pix = fitz.Pixmap(pdf_doc, xref)
                    image_name = f"{img_folder_path}/p{page} x{xref}.png"

                    # Save images depending on color map type. -----------------
                    if pix.n - pix.alpha < 4:
                        # This ^ pixel size is gray or RGB.
                        pix.writePNG(image_name)
                        print(f"Saved image: {image_name}")
                    else:
                        # Otherwise it's CMYK. So convert to RGB first.
                        pix_fix = fitz.Pixmap(fitz.csRGB, pix)
                        print(f"Converting CMYK image {pix}..")
                        pix_fix.writePNG(image_name)
                        print(f"Saved image: {image_name}")

            except RuntimeError:
                print(f"\n/////////// Image Extract: Cannot retrieve page info "
                      f"for page {page} in {self.file_name}.\n")
                continue

    def text_extract_separated(self):
        # Extract text from all pages in a PDF,
        # and split it out to separate text files per page.

        # New folder for extracted pages.
        text_folder_path = f"{self.directory}/extracted text"
        try:
            os.makedirs(text_folder_path)
        except FileExistsError:
            pass

        # Open PDF as object to start. -----------------------------------------
        with open(self.pdf_full_path, 'rb') as pdf_file:
            reader = PyPDF4.PdfFileReader(pdf_file)
            self.page_amt = reader.numPages
            print(f"\nFound {self.page_amt} pages in {self.file_name}.\n")

            # Extract text on each page.
            for p in range(1, reader.numPages):
                page = reader.getPage(p)

                try:
                    extracted_text = page.extractText()
                except KeyError:
                    print(f"\n/////////// Text Extract: "
                          f"'extractText' resulted in a Key Error on page "
                          f"{p} of {pdf_file}.\n")
                    continue

                # Save text extracts to txt files.
                with open(f"{text_folder_path}/{self.file_name[:-4]} page {p}.txt",
                          "w", encoding="utf-8") as text_page:

                    print(f"Creating text file of page {p} of {reader.numPages} "
                          f"to {self.file_name[:-4]} page {p}.txt.")
                    text_page.write(f"\n\n\n\n"
                                    f"---------------------------- "
                                    f"Page {p} of {reader.numPages} "
                                    f"----------------------------"
                                    f"\n\n\n\n"
                                    f"{extracted_text}")

    def text_extract_combined(self):
        # Extract text from all pages in a PDF,
        # and combine it all into one text file.

        # New folder for extracted pages.
        text_folder_path = f"{self.directory}/extracted text"
        try:
            os.makedirs(text_folder_path)
        except FileExistsError:
            pass

        # Open PDF as object to start. -----------------------------------------
        with open(self.pdf_full_path, 'rb') as pdf_file:
            reader = PyPDF4.PdfFileReader(pdf_file)
            self.page_amt = reader.numPages
            print(f"\nFound {self.page_amt} pages in {self.file_name}.\n")

            # Extract text on each page.
            for p in range(1, reader.numPages):
                page = reader.getPage(p)

                try:
                    extracted_text = page.extractText()
                except KeyError:
                    print(f"\n/////////// Extracting text failed on page "
                          f"{p} of {pdf_file}.\n")
                    continue

                # Save text extracts to text file, append.
                with open(f"{text_folder_path}/{self.file_name[:-4]} full.txt",
                          "a", encoding="utf-8") as text_page:

                    if len(extracted_text) > 0:
                        text_page.write(f"\n\n\n\n"
                                        f"---------------------------- "
                                        f"Page {p} of {reader.numPages} "
                                        f"----------------------------"
                                        f"\n\n\n\n"
                                        f"{extracted_text}")

                        print(f"Adding text from page {p} of {reader.numPages} "
                              f"to {self.file_name[:-4]} full.txt.")

                    elif len(extracted_text) == 0:
                        text_page.write(f"\nMISSING OR NO TEXT ON PAGE "
                                        f"{p} of {reader.numPages}.\n")

                        print(f"/////// Page {p} of {reader.numPages} "
                              f"in {self.file_name} did not generate any text.")

    def tesseract_extract(self):
        # TODO:
        #     Find text in extracted or provided images and extract it
        #     using PyTesseract.
        #     https://github.com/madmaze/pytesseract
        pass


# Functions --------------------------------------------------------------------
def run_extracts(*pdfs):
    # Take in pdf class instances and run each method I want.
    # This way I don't have to copy/paste calling methods over and over
    # for every instance I make for each PDF I wanna analyze.

    for pdf in pdfs:
        # pdf.text_extract_separated()
        try:
            pdf.text_extract_combined()
            pdf.image_extract()
            pdf.tesseract_extract()

        except PyPDF4.utils.PdfReadError:
            print(f"PDF hasn't been decrypted according to PyPDF4.")


def find_pdfs(file_path):
    # Walk directory to find files that end with "pdf".
    # Instantiate PDFAnalyzer class, then run our pdf methods.

    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file.endswith(".pdf"):
                instance = PDFAnalyzer(root, file)
                run_extracts(instance)


def main():

    while True:
        try:
            path = input("Enter path to search for and convert all PDFs. ")
            find_pdfs(path)
            break

        except FileNotFoundError:
            print("Couldn't find that folder! Did you enter it correctly?")
            continue

    print(f"\nComplete! Check log files at {log_folder}.\n")


# Start ------------------------------------------------------------------------
main()