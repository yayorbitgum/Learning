# "Wouldn’t it be trivially simple for algorithms to ignore the text after the
# + and before the @ when they sell your email?"
#
# I think so yes!


email_1 = 'leak+paypal@gmail.com'
email_2 = 'leak+bank3e+w+fd+k@gmail.com'
email_3 = 'leak+my+favorite+egirl@gmail.com'

emails = [email_1, email_2, email_3]
cleaned = []

# This is assuming we start with a database of verified emails, as would likely
# be the case in a data leak. So no need for complicated email regex.
for email in emails:
    if '+' in email:
        blocks = email.split('+')
        name = blocks[0]
        domain_split = blocks[-1].split('@')
        domain = domain_split[-1]

        clean = f"{name}@{domain}"
        cleaned.append(clean)

print(emails)
print(cleaned)