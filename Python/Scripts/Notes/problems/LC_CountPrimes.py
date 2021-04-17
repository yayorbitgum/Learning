# https://leetcode.com/explore/interview/card/top-interview-questions-easy/102/math/744
# https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes#Example

class Solution:

    def countPrimes(self, n: int) -> int:
        """Sieve of Eratosthenes."""
        if n < 2:
            return 0

        # "1" indicates a prime number. Easy to count after too.
        sieve = [1] * n
        # We know two and zero are not primes.
        sieve[0] = 0
        sieve[1] = 0
        # The smallest factor of a non-prime won't be greater than the square root of n.
        upper = int(n**0.5) + 1

        for num in range(2, upper):
            if sieve[num] != 0:
                # Step size for the loop is num's multiple.
                for not_prime in range(num*num, n, num):
                    sieve[not_prime] = 0

        # Each "1" indicates a prime number so we can just sum it.
        return sum(sieve)


expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
test = Solution()

assert test.countPrimes(45) == len(expected)