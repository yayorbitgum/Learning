# https://leetcode.com/explore/interview/card/google/67/sql-2/3044/
# Unique Email Addresses.
# Somehow got this on the first try let's go.
# Second attempt I cut runtime from 128ms to 72ms. Still not the best but not bad.
from typing import List


class Solution:
    def numUniqueEmails(self, emails: List[str]) -> int:
        actual_emails = []

        for email in emails:
            # Reset our flags and result string before checking the next email.
            ignore_after_plus = False
            actual_email = ''

            for ch in email:
                if ch == '@':
                    # We want to take everything in the domain (everything after @)
                    # and stop the ch loop here to save time.
                    domain = email.split('@')
                    actual_email += f"@{domain[1]}"
                    break

                elif not ignore_after_plus and ch != '.':
                    if ch == '+':
                        # We want to toggle this so we can ignore anything
                        # after a + sign, but before the @domain.
                        ignore_after_plus = True
                    else:
                        # Now we take in everything that isn't a dot, before
                        # the domain comes up.
                        actual_email += ch

            actual_emails.append(actual_email)

        return len(set(actual_emails))


test_input = ["test.email+alex@leetcode.com",
              "test.email.leet+alex@code.com"]
test = Solution()
print(test.numUniqueEmails(test_input))