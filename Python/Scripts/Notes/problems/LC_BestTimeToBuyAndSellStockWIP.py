# https://leetcode.com/problems/best-time-to-buy-and-sell-stock/submissions/
# This solution *does* work for 190/210 test cases, but fails at 191 for time exceeded.
# I need to figure out a more efficient way to do this.
# Really don't want to look up answers lol.
from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        profits = []
        if len(prices) == 1:
            return 0

        for index, buy in enumerate(prices):
            try:
                if buy < prices[index+1]:
                    # We'll only check a sale profit for any price after the buy.
                    for sell in prices[index+1:]:
                        transaction = sell-buy
                        if transaction > 0:
                            profits.append(transaction)
            except IndexError:
                # We'll only reach here if we've reached the end of prices.
                break

        return max(profits) if profits else 0


problem = [2, 4, 1]
test = Solution()
print(test.maxProfit(problem))