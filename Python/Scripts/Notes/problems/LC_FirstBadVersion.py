# https://leetcode.com/explore/interview/card/top-interview-questions-easy/96/sorting-and-searching/774/
# Sorting and Searching: First Bad Version

# The isBadVersion API is already defined for you.
# @param version, an integer
# @return an integer
def isBadVersion(version):
    if version >= 1702766719:
        return True
    else:
        return False


# To solve this one, I referenced my notes in algorithms/simple_binary_search_algorithm.py.
class Solution:
    def firstBadVersion(self, n):
        latest_version = n
        earliest_version = 1

        # This is to avoid the one worst possible time complexity case.
        if isBadVersion(earliest_version):
            return earliest_version

        # Binary search!
        while earliest_version < latest_version:
            # If we've narrowed it down to two versions right next to each other, we've got our answer.
            if latest_version - earliest_version == 1:
                return latest_version

            # We'll cut our search in half every time here.
            middle_guess = (latest_version + earliest_version) // 2
            if isBadVersion(middle_guess):
                # If the middle is a bad version, then we know it's this or earlier,
                # so make this the new upper limit and search again.
                latest_version = middle_guess
            else:
                # If the middle is a good version, then we're too early, so
                # we move the lower limit up to here.
                earliest_version = middle_guess


test = Solution()
print(test.firstBadVersion(2126753390))