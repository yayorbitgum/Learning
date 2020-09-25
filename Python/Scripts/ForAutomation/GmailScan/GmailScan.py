# A basic script that checks for unread emails from or about EVGA.
#
# Check the Quickstart guide:
# https://pypi.org/project/EZGmail/
# Using this requires some initial setup from:
# https://developers.google.com/gmail/api/quickstart/python
# to first grab the credentials file, then to get token.pickle from Google.

import ezgmail
from googleapiclient.errors import HttpError
from playsound import playsound
from time import sleep

print("Watching for messages from EVGA.. ")
count = 0

while True:
    try:
        unread_threads = ezgmail.unread()
    except HttpError:
        print("HTTP Error occurred. Rate limit probably exceeded. "
              "Waiting for some time.")
        sleep(1800)
        continue

    count += 1
    if count % 2 == 0:
        print('beep boop..')
    else:
        print('boop beep!')

    if count % 10 == 0:
        print("Watching for messages from EVGA.. ")

    # For every gmail thread..
    for thread in unread_threads:
        # For every message in that thread..
        for message in thread.messages:
            # messages[n] objects have the following attributes:
            # .sender
            # .recipient
            # .subject
            # .body
            # .timestamp
            # If "EVGA" is anywhere in the body of that message:
            if "evga" in message.body.lower():
                # Let me know!
                print(f"----\n"
                      f"Sender: {message.sender}"
                      f"\n----\n"
                      f"Subject: {message.subject}"
                      f"\n----\n"
                      f"Body: {message.body}")
                playsound('G:\Ableton Exports\SoundEffects\smol_notify.mp3')

    sleep(60)