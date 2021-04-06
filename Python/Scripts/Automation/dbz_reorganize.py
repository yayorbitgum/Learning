# Wrote a quick script to rename and reorganize a torrent of DBZ episodes.

import os
import shutil

dbz_folder = 'M:\Torrents\Shows\Dragonball Z Complete Series'

for root, dirs, files in os.walk(dbz_folder):
    print(root)

    for file in files:
        if file.startswith('Episode  '):
            # Removed unnecessary prefix for better name sorting.
            file_new = file.removeprefix('Episode  ')
            path_old = os.path.join(root, file)
            path_new = os.path.join(root, file_new)

            os.rename(path_old, path_new)
            # Saga subfolders were unnecessary nested organization, so we
            # move all episodes to root now that all prefixes are episode numbers.
            shutil.move(path_new, f"{dbz_folder}/{file_new}")