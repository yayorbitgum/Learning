# https://www.codewars.com/kata/5f7c38eb54307c002a2b8cc8/python
# "Your task is to remove everything inside the parentheses
#   as well as the parentheses themselves [from a string]."
#
# I think this is the first time I've ever used recursion, so I'm gonna save this
# solution even if it's inefficient.


def remove_parentheses(s: str):
    count = 0
    start = 0
    end = 0

    if "(" in s:
        for i, ch in enumerate(s):
            if ch == "(":
                count += 1
                if count < 2:
                    # We spot our first open parenthesis and grab that index.
                    start = i

            elif ch == ")":
                # Decrease for each matching closing parenthesis.
                count -= 1
                if count == 0:
                    # Once all accounted for, we know that's the last closed.
                    # Grab that index too.
                    end = i
                else:
                    continue

        # The above works (for (nested)), but for (separate) (groups),
        # we need to run it through again and again.
        # So pass in our string again, minus the sliced out bit.
        s = remove_parentheses(s[0:start] + s[end + 1:])
        return s

    else:
        return s


print(remove_parentheses('a(b(c))'))