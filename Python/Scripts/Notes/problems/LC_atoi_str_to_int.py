# https://leetcode.com/explore/interview/card/top-interview-questions-easy/127/strings/884/
# This problem wants to keep the value within 32b signed int range, so for
# python I'll need some arbitrary capping on conversion.
#  -2,147,483,648 to +2,147,483,647
import re


class Solution:

    def atoi(self, s: str) -> int:
        lower_limit = -2_147_483_648
        upper_limit = 2_147_483_647
        s = s.strip()

        if len(s) > 0:

            if s.startswith('+-') or s.startswith('-+'):
                return 0
            # If, for example, the string starts with words:
            if not s[0].isnumeric() and s[0] != '-' and s[0] != '+':
                return 0

            # Matches all digits of any length, optionally preceding with '-' or '+'.
            match = re.match('(-?\+?\d*)', s)
            result = match.group(0)

            try:
                result = int(result)
            except ValueError:
                return 0

            if result < lower_limit:
                return lower_limit
            elif result > upper_limit:
                return upper_limit
            else:
                return result

        return 0


tests = ["-+42",
         "   -42",
         "  4193 with words",
         "  words and 987",
         "-91283472332",
         "",
         "-",
         "+1",
         " "]

solve_me = Solution()
for test in tests:
    print(solve_me.atoi(test))