class Solution:
    def strStr(self, haystack: str, needle: str) -> int:

        if len(needle) == 0:
            return 0
        if needle in haystack:
            return haystack.index(needle)

        return -1


# Test cases! ------------------------------------------------------------------
test = Solution()
ex1 = ['hello', 'll']
ex2 = ['aaaaa', 'bba']
ex3 = ['', '']
examples = [ex1, ex2, ex3]

for example in examples:
    print(test.strStr(example[0], example[1]))