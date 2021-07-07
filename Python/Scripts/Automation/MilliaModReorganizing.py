# Wrote a quick script to rename and reorganize a torrent of DBZ episodes.

import os
import shutil

GGStrive_folder = 'S:\Games\Steam\steamapps\common\GUILTY GEAR STRIVE\RED\Content\Paks\~mods'

for root, dirs, files in os.walk(GGStrive_folder):
    print(root)

    for file in files:
        if file.lower().__contains__("millia"):
            replaced = file.lower().replace("millia", "")
            fixed = "Millia - " + replaced
            path_old = os.path.join(root, file)
            path_new = os.path.join(root, fixed)
            print(path_old)
            print(path_new)
            print()
            os.rename(path_old, path_new)