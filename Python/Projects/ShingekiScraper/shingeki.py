# Scrapes and downloads all images from readnsk.com for Attack on Titan.
# Organizes saved images by chapter and page in folders.
#
# Personal notes/references. ---------------------------------------------------
# Dissecting HTML pages with BeautifulSoup:
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# Getting all images on a page:
# https://stackoverflow.com/questions/18408307/how-to-extract-and-download-all-images-from-a-website-using-beautifulsoup
# Saving image data to a file:
# https://stackoverflow.com/questions/54338681/how-to-download-images-from-websites-using-beautiful-soup

# Imports. ---------------------------------------------------------------------
import os
import requests
from bs4 import BeautifulSoup
from requests.exceptions import MissingSchema

# Variables. -------------------------------------------------------------------
ch_number = 0
ch_count = 0
confirmation = False
root = os.path.abspath(os.curdir)


# Functions. -------------------------------------------------------------------
def format_check(ch_num: int) -> str:
    """
    Formats page number to three digits. Returns new string.
    Used for generating URLs for scraping, and for formatting for saving files.
    """
    ch_num = f"{ch_num}"
    if ch_num == "0":
        # https://ww7.readsnk.com/chapter/shingeki-no-kyojin-chapter-0/
        # compared to
        # https://ww7.readsnk.com/chapter/shingeki-no-kyojin-chapter-001/
        # So if it's chapter zero, don't format.
        return ch_num

    while len(ch_num) < 3:
        ch_num = "0" + ch_num

    return ch_num


def get_chapter_count(soup_obj: BeautifulSoup) -> int:
    """
    Get a chapter count indirectly from the dropdown menu on the first page.
    Return chapter count.
    """
    ch = []
    for o in soup_obj.find_all('option'):
        if "chapter" in o['value']:
            ch.append(o)

    # There are multiple dropdown menus (top and bottom) so let's remove duplicates.
    length = len((dict.fromkeys(ch)))

    return length


# Chapter loop. ----------------------------------------------------------------
# TODO: Break all of this apart into more modular components/functions.
while True:
    # Reset page number and count for each chapter.
    page_number = 1
    count = 0

    ch_format = format_check(ch_number)
    ch_url = f'https://ww7.readsnk.com/chapter/shingeki-no-kyojin-chapter-{ch_format}/'
    req = requests.get(ch_url)

    # "OK" status confirm to start. --------------------------------------------
    if req.status_code == 200:

        soup = BeautifulSoup(req.content, 'html.parser')
        # Each chapter will be separated with their own folders.
        ch_path = f"{root}/shingeki/chapter{ch_format}"
        try:
            os.makedirs(ch_path)
        except FileExistsError:
            print(f"Directory exists for {ch_path}.")

        if not confirmation:
            chapters = get_chapter_count(soup)
            # Most chapters average 25-30mb in folder size.
            input(f"There are ~{chapters} chapters available. \n"
                  f"Total download size may be around {(30 * chapters) / 1000}GB or larger."
                  f"\nHit enter to proceed.")
            confirmation = True

        # Manga page loop. -----------------------------------------------------
        # All manga pages are images.
        img_tags = soup.find_all('img')
        for img in img_tags:
            try:
                # The img class for the manga pages seems to always be this type.
                if img['class'] == ['my-3', 'mx-auto', 'js-page']:
                    # Grab image url from src tag.
                    url = img['src'].rstrip('\r')

                    # Save manga page. -----------------------------------------
                    page_number += 1
                    pg_format = format_check(page_number)
                    with open(f"{ch_path}/Shingeki_{ch_format}_{pg_format}.png", 'wb') as file:
                        print(f"Downloading {url}...")
                        try:
                            image_response = requests.get(url)
                            file.write(image_response.content)
                            count += 1
                        except MissingSchema:
                            print(f"(404) Unable to find that image.\nSkipping!\n")

            except KeyError:
                # Very rarely, a chapter may contain an image (ad) that has no key 'class'.
                print(f"Skipping: {img['src']} (ad).")

        print(f"Finished chapter {ch_number}. Saved {count} pages.")
        ch_number += 1
        ch_count += 1

    # Else "Not found" (404) status. -------------------------------------------
    elif req.status_code == 404:
        print(f"You downloaded a total of {ch_count} chapters.\n\n")
        print(f"Unable to locate chapter {ch_number} of Shingeki at\n {ch_url}")
        print(f"Does that chapter exist yet?\n"
              f"If it does exist, check for differences in the URLs for this chapter.")

        # Open folder in explorer to see results (only works in Windows).
        os.startfile(root)
        break