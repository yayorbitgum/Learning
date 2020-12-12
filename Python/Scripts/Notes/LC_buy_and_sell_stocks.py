from typing import List


class Solution:
    def max_profit(self, prices: List[int]):
        profit = 0
        amt_of_trades = len(prices)

        for trade in range(1, amt_of_trades):
            # Only add gains together until we reach our max price.
            # So here we're only taking in positive gains.
            # Subtract previous trade from current trade each time.
            profit += max(prices[trade] - prices[trade-1], 0)

        return profit


ex1 = [7, 1, 5, 3, 6, 4]
ex2 = [1, 2, 3, 4, 5]
ex3 = [7, 6, 4, 3, 1]
ex4 = [1, 2]
ex5 = [1, 2, 4]
examples = [ex1, ex2, ex3, ex4, ex5]
test = Solution()

for example in examples:
    print(example)
    print(test.max_profit(example))