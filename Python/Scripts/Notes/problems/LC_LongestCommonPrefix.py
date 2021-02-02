# https://leetcode.com/explore/interview/card/top-interview-questions-easy/127/strings/887/
# Longest Common Prefix
from typing import List

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:

        # I want to sort by shortest string first so we can break the loop sooner,
        # in case a whole word is the whole prefix.
        strs.sort(key=len)
        prefix = ''
        if len(strs) == 0:
            return ''
        if len(strs) == 1:
            return strs[0]
        # We're going to check each letter of each word, in order (via indexes).
        longest = len(max(strs))

        if longest == 0:
            # This will catch any lists of empty strings.
            return ''

        for index in range(longest):
            # Reset these values for each loop.
            letter = ''
            words_checked = 0
            letters = []
            # Check each word.
            for word in strs:
                words_checked += 1
                try:
                    # Grab current letter.
                    letter = word[index]
                except IndexError:
                    # Reaching here means a whole word is the prefix,
                    # and we've already found it. This is why we sorted by length earlier.
                    return prefix
                # Add the current letter to the list of letters. We want them all
                # to match if it is a common prefix.
                letters.append(word[index])
                if letters.count(letter) != words_checked:
                    # We'll reach here if there's a mismatch of a letter at any point,
                    # So we can stop the loop from running more than it needs to.
                    break
            # ex: If we've got 4 A's and 4 words, then we know 'A' is part of the prefix.
            if letters.count(letter) == len(strs):
                prefix += letter
            else:
                # If it's a mismatch, then we've completed the prefix and shouldn't
                # add anymore letters to it.
                return prefix

        # Only going to reach down here if every single word is identical,
        # so the above loop fully completes.
        return prefix


# Testing!
test = Solution()
case1 = ["flower","flow","flight"]
case2 = ["anticlimax", "antiaircraft", "antiseptic", "antibody"]
case3 = ["companion", "commingle", "contact", "concentrate"]
case4 = ["ab", "a"]
case5 = ["",""]
case6 = ["flower","flower","flower","flower"]
cases = [case1, case2, case3, case4, case5, case6]
for case in cases:
    print(test.longestCommonPrefix(case))