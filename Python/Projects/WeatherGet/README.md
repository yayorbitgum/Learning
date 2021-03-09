This script pulls from _openweathermap.org_ API to display weather forecasts for whatever location you enter.

Your forecast is displayed in a neat console-based UI!

Data is pulled from https://openweathermap.org/forecast5.


1.) To make (free) API requests, make sure you register and grab an API key. Place it in "config.py".
2.) Make sure you pip install the following:
- _pip install requests_
- _pip install rich_ 
- _pip install fuzzywuzzy_

3.) **Download the list of cities** from openweathermap to allow for fuzzy matching your input when their API doesn't like what you entered!
- http://bulk.openweathermap.org/sample/city.list.json.gz _(3.8mb download, 40mb when unzipped)_

3a.) _And for faster fuzzy matching based on C++, pip install the following:_
- _python-Levenshtein_
