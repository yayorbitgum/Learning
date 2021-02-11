# https://leetcode.com/submissions/detail/454885381/?from=explore&item_id=3636
# "Your runtime beats 98.22% of python3 submissions."
# Yesss.

class Solution:
    def is_anagram(self, s: str, t: str) -> bool:

        # If the strings are different lengths, we might as well stop right away.
        if len(s) == len(t):
            # Keeping count with dictionaries.
            s_counts = {}
            t_counts = {}

            # We'll count unique characters only to avoid recounting the same letters.
            for ch in set(s):
                s_counts[ch] = s.count(ch)

            for ch in set(t):
                t_counts[ch] = t.count(ch)

            if s_counts == t_counts:
                return True

        return False


# ------------------------------------------------------------------------------
string_a = "aacc"
string_b = "ccac"
test = Solution()
print(test.is_anagram(string_a, string_b))