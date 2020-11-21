# I'm not sure what I want to do with this yet.
# For now I'm testing out mouse clicks, locating buttons on screen via
# image reference, and exploring options.

# Run following in console for retrieving coord and color info on cursor:
# pyautogui.mouseInfo()

import pyautogui
from time import sleep

# PyAutoGUI limit on all actions. Default is 0.01.
pyautogui.PAUSE = 0.01

# Contains width and height of current screen in pixels.
wh = pyautogui.size()
print(f"Screen resolution is {wh}.")

# This is a small image of the "X" in Mozilla where you close tabs.
# Seems to detect every button accurately despite small color variations. Very cool.
button_locs = pyautogui.locateAllOnScreen('image_ref/tab_close_x.png')

if button_locs is not None:
    for button in button_locs:
        print(f"Located button at: {button}")
        pyautogui.moveTo(button)
        sleep(1)
else:
    print("Unable to locate any matches on screen.")
