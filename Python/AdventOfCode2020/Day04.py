# https://adventofcode.com/2020/day/4
# https://regex101.com/r/tnEyIc/4
import re

# My glorious, unused regex:
regex = re.compile('(byr:\d{4})?|'                  # [0]  byr: xxxx
                   '(iyr:\d{4})?|'                  # [1]  iyr: xxxx
                   '(hgt:\d{2,3}(cm|in)?)?|'        # [2]  hgt: xxx cm / in
                   '(eyr:\d{4})?|'                  # [4]  eyr: xxxx
                   '(ecl:(\w{3,6}|#(\w{6})))|'      # [5]  ecl: xxx / #xxxxxx
                   '(hcl:(\w{3,6}|#(\w{6})))?|'     # [8]  hcl: xxx / #xxxxxx
                   '(cid:\d{1,3})?|'                # [11] cid: xxx
                   '(pid:\d{7,10})?|'               # [12] pid: xxxxxxxxxx
                   '(hcl:z)?'                       # [13] hcl: z (outlier)
                   '([\n][\n])')                    # [14] blank line

with open('inputs\day04_input.txt', 'r') as file:
    file = file.read().strip()

passports = file.split('\n\n')
keys = ['byr', 'ecl', 'eyr', 'hcl', 'hgt', 'iyr', 'pid']
passport_master_list = []
valid_count = 0

# Formatting messy input into nice clean dictionaries --------------------------
for passport in passports:
    fields = re.split('\s', passport)
    passport_dictionary = dict(entry.split(':') for entry in fields)
    passport_master_list.append(passport_dictionary)

# Part one! --------------------------------------------------------------------
for passport in passport_master_list:
    left_overs = keys[:]
    for key in passport.keys():
        if key in left_overs:
            left_overs.remove(key)

    if left_overs == 'cid':
        valid_count += 1

    elif len(left_overs) == 0:
        valid_count += 1

print(valid_count)