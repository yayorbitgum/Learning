# Simple script to remove Volume prefix from some chapter folders on OPM download,
# since the newer chapters haven't been placed into volumes yet.
import os
import re

opm_dir = "M:\OnePunchMan"
os.chdir(opm_dir)
# This should match 'Vol. xx' prefix as group 0, and everything after as group 1.
vol_regex = re.compile('(Vol. \d\d )(.*)')

for file in os.listdir(opm_dir):
    if vol_regex.match(file):
        path = re.findall(vol_regex, file)
        # I don't know why, but this regex is returning 3 groups.
        # Essentially, a one-item list [0] with a two-item tuple as the one item.
        # This means I need to unpack the tuple inside the first item in the list.
        prefix, new_name = path[0]
        os.rename(file, new_name)