#! python3
# shingeki.py - Download every single shingeki no kyojin comic
#
# Dissecting HTML pages with BeautifulSoup:
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# Getting all images on a page:
# https://stackoverflow.com/questions/18408307/how-to-extract-and-download-all-images-from-a-website-using-beautifulsoup
# Saving image data to a file:
# https://stackoverflow.com/questions/54338681/how-to-download-images-from-websites-using-beautiful-soup

import requests
from bs4 import BeautifulSoup
import webbrowser
import pyinputplus as pyip

# url = 'https://ww7.readsnk.com/chapter/shingeki-no-kyojin-chapter-'
#
#
# def chapter_request():
#     chapter = input("Please enter the chapter number you would like to read (ex: 001 = chapter 1): ")
#     newUrl = url + chapter
#     return newUrl
#
#
# def get_chapter():
#     while True:
#         user_choice = pyip.inputYesNo(prompt='Would you like to download this manga?: ')
#         if user_choice == 'yes':
#             res = requests.get(chapter_request())
#             res.raise_for_status()
#             playfile = open('shingekinokyojin.jpg', 'wb')
#         else:
#
#             webbrowser.open(chapter_request())
#
#
# chapter_request()
# get_chapter()


def format_check(chapter_or_page):
    # Ensures the length of the chapter or page number is always 3 digits long,
    # Because that's how the website formats their URL for each chapter.
    ch_num_format = chapter_or_page

    if len(str(chapter_or_page)) == 1:
        ch_num_format = f"00{chapter_or_page}"

    elif len(str(chapter_or_page)) == 2:
        ch_num_format = f"0{chapter_or_page}"

    return ch_num_format


# Setting our variables that will increase over time.
ch_num = 0

# Main loop. Should run once for each chapter.
while True:
    # Reset page number and count for each chapter.
    page_number = 1
    count = 0
    # Increase chapter number each loop.
    ch_num += 1

    # Get URL with requests.
    req = requests.get(f'https://ww7.readsnk.com/chapter/shingeki-no-kyojin-chapter-{format_check(ch_num)}/')

    # Make the BeautifulSoup object (parse the html) from req so we can parse it.
    soup = BeautifulSoup(req.content, 'html.parser')

    # Get all image tags in the page.
    img_tags = soup.find_all('img')

    for img in img_tags:
        page_number += 1
        # Filter out anything that isn't a manga page image.
        # The manga img class just happens to equal this list.
        if img['class'] == ['my-3', 'mx-auto', 'js-page']:
            # Grab the image url from "src" tag in html.
            url = img['src']

            # Format file name based on chapter and page numbers, open it.
            with open(f"Shingeki_{format_check(ch_num)}_{format_check(page_number)}.png", 'wb') as file:
                print(f"Downloading {url}...")
                # Stream in image data.
                image_response = requests.get(url, stream=True)
                # Write the image content to the file.
                file.write(image_response.content)
                count += 1

    print(f"Finished chapter {ch_num}. Saved {count} pages!")
