# https://www.khanacademy.org/math/algebra2/x2ec2f6f830c9fb89:logs/x2ec2f6f830c9fb89:log-intro/v/logarithms
# I wanted to see if I could figure out the logarithm using a function
# while following this Intro to Logarithms tutorial series.


def find_logarithm(base, result):
    """ This returns "log" in log(base_num)result.
        Example: log(3) 81 = return value, or 3^x = 81.
        This would be really slow for large log numbers since it starts from 1.
        TODO: Implement a binary search for finding the logarithm maybe?
    """
    x = 1
    # --------------------------------------------------------------------------
    # Any number raised to the power of 0 results in 1.
    if result == 1:
        return 0

    # --------------------------------------------------------------------------
    # Solves fractional results, ie negative logs.
    if 0 < result < 1:
        while True:
            check = 1 / (base ** x)
            if check == result:
                return -x
            else:
                x += 1

    # --------------------------------------------------------------------------
    # If the base is larger than result, then we know log is a 1/x fraction.
    if base > result:
        while True:
            if base ** (1 / x) == result:
                return 1 / x
            else:
                x += 1

    # --------------------------------------------------------------------------
    while True:
        # For whole number logs.
        if base ** x == result:
            return x

        else:
            # Slow!
            x += 1


# Tests ------------------------------------------------------------------------
print(find_logarithm(2, 128))
# print(find_logarithm(100, 1))     # log(anything) 1 = 0
# print(find_logarithm(8, 2))       # log(8) 2 = 1/3
# print(find_logarithm(2, 1/8))     # 2^x =  1/8, in this case x will be negative.
# print(find_logarithm(8, 1/2))     # TODO: 8^x = 1/2, in this case x will be a negative fraction -1/3.
# print(find_logarithm(2, 640))     # TODO: ??
# print(find_logarithm(2, -4))      # TODO: Find log of negative results.