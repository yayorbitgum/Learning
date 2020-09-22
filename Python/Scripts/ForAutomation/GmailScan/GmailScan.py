# A basic script that checks for unread emails from or about EVGA.
#
# Check the Quickstart guide:
# https://pypi.org/project/EZGmail/
# Using this requires some initial setup from:
# https://developers.google.com/gmail/api/quickstart/python
# to first grab the credentials file, then to get token.pickle from Google.

import ezgmail
from playsound import playsound

print("Watching for messages from EVGA.. ")
count = 0

while True:
    unread_threads = ezgmail.unread()
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
