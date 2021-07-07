import os

ggs_folder = 'S:\Games\Steam\steamapps\common\GUILTY GEAR STRIVE\RED\Content\Paks\~mods'

count = 0

for root, dirs, files in os.walk(ggs_folder):

    for file in files:
        if file.lower().__contains__("millia"):
            count += 1
            replaced = file.lower().replace("millia", "")
            fixed = "Millia - " + replaced
            path_old = os.path.join(root, file)
            path_new = os.path.join(root, fixed)
            os.rename(path_old, path_new)
            print(f"From -> {path_old}")
            print(f"To -> {path_new}\n")

if count == 0:
    print("No files found related to Millia.")