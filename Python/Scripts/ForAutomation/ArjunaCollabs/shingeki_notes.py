#! python3
# shingeki.py - Download every single XKCD comic.

import requests, os, sys
from bs4 import BeautifulSoup


def chapter_request():
    req_chapter = input('Which chapter would you like to read? ')
    if req_chapter == 'q':
        print('Exiting program.')
        sys.exit()
    return req_chapter


def format_check(chapter):          # Changed this.
    # Removed chapter_request() from here so it's not called every time we format.
    if len(str(chapter)) == 1:
        chapter = f"00{chapter}"
    elif len(str(chapter)) == 2:
        chapter = f"0{chapter}"
    return chapter


def main_program():
    url = 'https://ww7.readsnk.com/chapter/shingeki-no-kyojin-chapter-'

    # This is the per chapter loop. --------------------------------------------
    while True:
        chapter = chapter_request()     # Moved chapter variable and request here.
        res = requests.get(url + str(format_check(chapter)))    # Now format won't call input every time.
        soup = BeautifulSoup(res.content, 'html.parser')

        # Each manga page is an image, so grab all images.
        img_tags = soup.find_all('img')

        # This is the per page loop. -------------------------------------------
        for img in img_tags:
            # Each manga page image is this particular class:
            if img['class'] == ['my-3', 'mx-auto', 'js-page']:
                new_url = img['src']
                # TODO: Add an iterated value here. Something like count += 1.
                # You need a value to iterate (count up) every time the "for img" loops,
                #   or maybe just every time it finds a manga page in this "if" statement.
                # Otherwise you'll only save one image, because the file name below
                #   is only changing when the chapter changes.
                # So it just overwrites the last image every time as the same file.
                with open(f"Shingeki_{format_check(chapter)}.png", 'wb') as file:
                    print(f"Downloading {new_url}...")
                    # Fix URL here. It's the wrong variable.
                    image_response = requests.get(url, stream=True)
                    file.write(image_response.content)

        print(f"Finished chapter {chapter}. Saved {count} pages!")      # "count" is unused right now.


main_program()