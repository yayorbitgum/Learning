# https://leetcode.com/problems/count-items-matching-a-rule/
# "Runtime: 244 ms, faster than 100.00% of Python3 online submissions for Count Items Matching a Rule."
# Damn, this one turned out really fast I suppose hahah.
from typing import List


class Solution:
    def count_matches(self, items: List[List[str]], rule_key: str, rule_value: str) -> int:

        # items[index] = [type, color, name]
        keys = {'type': 0, 'color': 1, 'name': 2}
        matches = 0

        for item in items:
            if item[keys[rule_key]] == rule_value:
                matches += 1

        return matches


# ------------------------------------------------------------------------------
a_key   = 'color'
a_value = 'silver'
a_input = [["phone", "blue", "pixel"],
           ["computer", "silver", "lenovo"],
           ["phone", "gold", "iphone"]]

b_key   = 'type'
b_value = 'phone'
b_input = [["phone","blue","pixel"],
           ["computer","silver","phone"],
           ["phone","gold","iphone"]]

test = Solution()
print(test.count_matches(a_input, a_key, a_value))
print(test.count_matches(b_input, b_key, b_value))