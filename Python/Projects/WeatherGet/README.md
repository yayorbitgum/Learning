This script pulls from _openweathermap.org_ API to display weather forecasts for whatever location you enter.

Your forecast is displayed in a neat console-based UI!

Data is pulled from https://openweathermap.org/forecast5.

# To use, make sure you pip install the following:
- _requests_
- _rich_ 
- _fuzzywuzzy_

and **download the list of cities** from openweathermap to allow for fuzzy matching your input when their API doesn't like what you entered!
- http://bulk.openweathermap.org/sample/city.list.json.gz (3.8mb download, 40mb when unzipped)

_And for faster fuzzy matching based on C++, pip install the following:_
- _python-Levenshtein_
