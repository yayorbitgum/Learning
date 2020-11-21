# https://www.codewars.com/kata/514a024011ea4fb54200004b
# Gets the domain name in a URL string.
# This is so bad I should refactor this when I understand regex better.
# This should only take one regex line.
# It worked and passed the tests, but not nearly as succinct as other solutions.
import re


def domain_name(url):
    http_www_match = re.compile('(http://|www.|https://)(www.)?([^.]*)(\.)')
    http_re_search = http_www_match.search(url)

    name_only_match = re.compile('([^.^\W]*)(\.)([^/^\W]*)')
    name_only_search = name_only_match.search(url)

    if http_re_search:
        match = http_re_search.group(3)
        if match[:4] == "www.":
            return match.lstrip('www.')
        else:
            return match

    elif name_only_search:
        return name_only_search.group(1)

    else:
        return f"Didn't find {url}"


test_sites = [
    "http://github.com/carbonfive/raygun",
    "http://www.zombie-bites.com",
    "https://www.cnet.com",
    "http://google.com",
    "http://google.co.jp",
    "www.xakep.ru",
    "www.hyphen-site.com",
    "icann.com",
    "icann.org",
    "gnxcam4ep7pr4x0x2omy.com",
    "www.vekdur1jet2954ckwu678v07myctl.com",
    "www.pe1g6lml.jp",
    "https://www.codewars.com/kata/514a024011ea4fb54200004b/train/python",
    "https://youtube.com"]

for site in test_sites:
    print(domain_name(site))