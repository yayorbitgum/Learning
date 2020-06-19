# Test regex here. https://regex101.com/
#
# This program should be able to grab most phone numbers and emails from the clipboard,
# display the results, and copy the neatly formatted results to the clipboard too.


# //////////////////////////////////////// Imports ////////////////////
import pyperclip
import re


# //////////////////////////////////////// Regular Expressions ////////////////////
# Expression to grab phone numbers.
phone_regex = re.compile(r'(\d{3}|\(\d{3}\))?'            # Group 0: Area Code (optional): 555 or (555).
                         r'(\s|\.|-)?'                    # Group 1: Separator (optional): Spaces, periods or dashes.
                         r'(\d{3})'                       # Group 2: Prefix: 555. 
                         r'(\s|\.|-)'                     # Group 3: Separator.
                         r'(\d{4})'                       # Group 4: Line: 5555.
                         r'(,?\s*?'                       # Opening Group 5: Whole Extension (optional): ext. 55555
                         r'(ext|x|ext.|extension|ex)\s*'    # Sub-group 6: Extension prefix and spaces.
                         r'(\d{2,5})'                       # Sub-group 7: The extension numbers.
                         r')?'                            # Closing Group 5.
                         )

# Expression to grab email addresses.
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

    # For each phone number found with the regex scanning the clipboard content coming in:
    for phone in phone_regex.findall(user_clipboard):
        # If we have an extension indicator, ie regex group 6 isn't blank:
        if phone[6] != '':
            # Format and append to list, eg: 555.555.5555 ext 55555
            phone_num = f"{phone[0]}.{phone[2]}.{phone[4]}, ext {phone[7]}"
            phone_matches.append(phone_num)
        else:
            # Otherwise format and add to list, without extension.
            phone_num = f"{phone[0]}.{phone[2]}.{phone[4]}"
            phone_matches.append(phone_num)


def find_email_matches(user_clipboard):
    """
    Find email regex matches, then append to list.
    """

    # For each email address found in clipboard:
    for email in email_regex.findall(user_clipboard):
        # Add group 0 from the regex, which is just the whole email address.
        email_matches.append(email[0])


def copy_results_to_clipboard():
    """
    Reveal results and copy them to user clipboard, if there are any,
    then reset/clear the lists for next use.
    """

    # If either matches list is not empty:
    if len(email_matches) > 0 or len(phone_matches) > 0:

        # Join each result in the matches lists, to a string, with a new line \n.
        # We do this so we don't give the user the raw list format with brackets and everything.
        # .join() actually iterates! I didn't know that.
        ph_results = '\n'.join(phone_matches)
        em_results = '\n'.join(email_matches)
        # Combine and copy these results to the user's clipboard.
        pyperclip.copy(f"{ph_results}\n{em_results}")

        # Show us results were copied to the clipboard, for feedback.
        print(f"\nPhone Results:")
        for number in phone_matches:
            print(number)

        print(f"\nEmail Results:")
        for email in email_matches:
            print(email)

        print(f"\nCopied {len(email_matches)+len(phone_matches)} results to your clipboard.\n"
              f"Now you can paste it wherever you want.\n")

        # Finally, empty the lists to be re-used, so clipboard doesn't multiply with multiple runs.
        del email_matches[:]
        del phone_matches[:]

    # If neither regex found any matches, then the lengths will be zero, so we come here.
    else:
        print("///////////////////////////////////////////////////////////////////////"
              "\nNo phone number or email address was found in your clipboard content.\n"
              "///////////////////////////////////////////////////////////////////////")


def press_play():
    """
    This is our looping function to allow repeated use of the program until we quit.
    """
    print("This program will scan your clipboard content for any phone numbers and email addresses, "
          "then copy them to your clipboard as well as display the results.")

    while True:
        user_input = input("\nCopy the text you want to scan into your clipboard (CTRL+C). "
                           "\nIf it's already copied, hit enter to continue."
                           "\nYou can also enter q to quit.\n")

        if user_input != 'q':
            # Assign variable for our pasted clipboard that we'll pass into our functions.
            pasted_clipboard = str(pyperclip.paste())
            # Toss it into check_for_matches function.
            check_for_matches(pasted_clipboard)
            copy_results_to_clipboard()
        else:
            break


# //////////////////////////////////////// Program ////////////////////
press_play()
