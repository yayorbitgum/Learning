# Test regex here. https://regex101.com/
#
# This program should be able to grab most phone numbers and emails from the clipboard,
# display the results, and copy the neatly formatted results to the clipboard too.


# //////////////////////////////////////// Imports ////////////////////
import pyperclip
import re


# //////////////////////////////////////// Regular Expressions ////////////////////
# Expression to grab phone numbers.
# Example: +1 (555) 555-5555 ext 1234
phone_regex = re.compile(r'(\+\s*?\d{1,3})?\s*?'          # Group 0: Country code (optional): +1, + 23, etc.
                         r'(\d{3}|\(\d{3}\))?'            # Group 1: Area Code (optional): 555 or (555).
                         r'(\s|\.|-)?'                    # Group 2: Separator (optional): Spaces, periods or dashes.
                         r'(\d{3})'                       # Group 3: Prefix: 555. 
                         r'(\s|\.|-)'                     # Group 4: Separator.
                         r'(\d{4})'                       # Group 5: Line: 5555.
                         r'(,?\s*?'                       # Opening Group 6: Whole Extension (optional): ext. 55555
                         r'(ext|x|ext.|extension|ex)\s*'    # Sub-group 7: Extension prefix and spaces.
                         r'(\d{2,5})'                       # Sub-group 8: The extension numbers.
                         r')?'                            # Closing Group 6.
                         )

# Expression to grab email addresses.
# Example: johnruththehangman@wowee.gov
email_regex = re.compile(r'('                       # Start regex group 0.
                         r'[a-zA-Z0-9._%+-]+'       # Username [One or more+ characters that can be any shown here.]
                         r'@'                       # The @ symbol that's hopefully going to be present.
                         r'[a-zA-Z0-9.-]+'          # Domain name [similar to username matching], but happens after @.
                         r'(\.[a-zA-Z]{2,4})'       # dot (.), then 2-4 letters a through z: com, org, .etc
                         r')'                       # End regex group 0.
                         )
# The format for email addresses has a lot of weird rules.
# The above regular expression won’t match every possible valid email address,
# but it’ll match almost any typical email address you’ll encounter.


# //////////////////////////////////////// Lists ////////////////////
phone_matches = []
email_matches = []


# //////////////////////////////////////// Functions ////////////////////
def check_for_matches(user_clipboard):
    """
    Run our finding/formatting functions.
    Easy to expand here if we make more expressions and functions.
    """
    find_phone_matches(user_clipboard)
    find_email_matches(user_clipboard)


def find_phone_matches(user_clipboard):
    """
    Find phone regex matches and format them, then append to matches list.
    We can change phone formatting here to whatever we want, regardless of
    how they were originally formatted.
    """
    # For each phone number found with the regex scanning the clipboard content coming in,
    # after first removing duplicates from that list:
    for phone in remove_dupes(phone_regex.findall(user_clipboard)):
        # The way I format based on optional extensions and country codes seems really messy.
        # Feels too much like "choose your own adventure" here.
        # Not sure how to approach fixing that.

        # If there's a country code present:
        if phone[0] != '':
            # And if we have an extension indicator, ie regex group 7 isn't blank:
            if phone[7] != '':
                # Format and append to list, eg: +1 555.555.5555 ext 55555
                phone_num = f"{phone[0]} {phone[1]}.{phone[3]}.{phone[5]} ext {phone[8]}"
                phone_matches.append(phone_num)
            else:
                # Otherwise format and add to list, without extension.
                phone_num = f"{phone[0]} {phone[1]}.{phone[3]}.{phone[5]}"
                phone_matches.append(phone_num)

        # Otherwise if there's no country code:
        else:
            # And if we have an extension indicator, ie regex group 7 isn't blank:
            if phone[7] != '':
                # Format and append to list, eg: 555.555.5555 ext 55555
                phone_num = f"{phone[1]}.{phone[3]}.{phone[5]} ext {phone[8]}"
                phone_matches.append(phone_num)
            else:
                # Otherwise format and add to list, without extension.
                phone_num = f"{phone[1]}.{phone[3]}.{phone[5]}"
                phone_matches.append(phone_num)


def find_email_matches(user_clipboard):
    """Find email regex matches, then append to list."""
    # For each email address found in clipboard list, while removing duplicates:
    for email in remove_dupes(email_regex.findall(user_clipboard)):
        # Add group 0 from the regex, which is just the whole email address.
        email_matches.append(email[0])


def remove_dupes(clean_me):
    """
    This should remove any duplicate entries in the matches lists we pass in as the clean_me argument.
    Since we can't have duplicate keys in a dictionary, we convert the list to dictionary keys,
    then back to a list.
    """
    cleaned = list(dict.fromkeys(clean_me))
    return cleaned


def copy_results():
    """Copy all results to the user's clipboard, if there are any."""
    # If either matches list is not empty:
    if len(email_matches) > 0 or len(phone_matches) > 0:
        # Join each result in the matches lists, to a string, with a new line \n.
        # We do this so we don't give the user the raw list format with brackets and everything.
        # .join() actually iterates! I didn't know that.
        ph_results = '\n'.join(phone_matches)
        em_results = '\n'.join(email_matches)
        # Format for the clipboard result.
        glorious_result = f"{ph_results}\n{em_results}"

        # Since we'll copy the results to the clipboard, we'll always then want to
        #   - Show results for feedback so the user isn't confused about if anything even happened.
        #   - Clear the lists so we can run this as much as we want after.
        #   - Make sure we haven't just copied/pasted the same results from a previous run.
        check_me = str(pyperclip.paste())
        if sanity_check(check_me) != "oh no":
            # Combine and copy these results to the user's clipboard.
            pyperclip.copy(glorious_result)
            show_results()
            clear_matches()

        # If it is actually identical:
        elif sanity_check(check_me) == "oh no":
            sanity_confirm = input("\n\nWhoa there cowboy. You're checking the results of your last scan, "
                                   "so it's going to be identical.\n"
                                   "Are you sure you want to do this? y/n:\n")

            if sanity_confirm != 'n':
                # If yes, then go ahead and do it again for whatever reason.
                pyperclip.copy(glorious_result)
                show_results()
                clear_matches()
            else:
                # Else reset.
                print("---------------------------------------------------------------------------\n"
                      "Canceling...\n"
                      "---------------------------------------------------------------------------\n")
                clear_matches()

    # If neither regex found any matches, then the lengths will be zero, so we come here.
    else:
        print("///////////////////////////////////////////////////////////////////////"
              "\nNo phone number or email address was found in your clipboard content.\n"
              "///////////////////////////////////////////////////////////////////////")


def show_results():
    """Show us results were copied to the clipboard, for feedback."""
    print(f"\nPhone Results:")
    for number in phone_matches:
        print(number)

    print(f"\nEmail Results:")
    for email in email_matches:
        print(email)

    print(f"\nCopied {len(email_matches)+len(phone_matches)} results to your clipboard.\n"
          f"(Note, duplicates have been removed from results).\n"
          f"---------------------------------------------------------------------------\n")


def clear_matches():
    """
    Empty the lists to be re-used, so clipboard doesn't multiply with multiple runs.
    """
    del email_matches[:]
    del phone_matches[:]


def paste_clipboard():
    """Paste out current clipboard and return it."""
    pasted_clipboard = str(pyperclip.paste())
    return pasted_clipboard


def sanity_check(string_to_check):
    """
    Check if what we're scanning is what we generated previously.
    Returns "oh no" if it is identical.
    """
    ph_results = '\n'.join(phone_matches)
    em_results = '\n'.join(email_matches)
    glorious_result = f"{ph_results}\n{em_results}"

    if string_to_check == glorious_result:
        return "oh no"


def press_play():
    """
    This is our looping function to allow repeated use of the program until we quit.
    """
    print("----------------------------------------------------------------------------------------\n"
          "This program will scan your clipboard content for any phone numbers and email addresses,\n"
          "then copy them to your clipboard as well as display the results.")

    while True:
        user_input = input("\nCopy the text you want to scan into your clipboard (CTRL+C). "
                           "\nIf it's already copied, hit enter to continue."
                           "\nYou can also enter q to quit.\n").strip()

        if user_input != 'q':
            # Check for matches in our pyperclip pasted clipboard.
            check_for_matches(paste_clipboard())
            copy_results()
        else:
            break


# //////////////////////////////////////// Program ////////////////////
press_play()
