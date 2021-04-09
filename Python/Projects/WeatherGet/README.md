This script pulls from _openweathermap.org_ API to display weather forecasts for whatever location you enter.

Your forecast is displayed in a neat console-based UI!

Data is pulled from https://openweathermap.org/forecast5.

# Installation ->
- **To make (free) API requests, make sure you register and grab an API key at**  
  https://openweathermap.org/api. 
  - Hit subscribe on any, and pick free tier.
  - Place key in "config.py".  
- **For required modules**: 
  - _pip install -r requirements.txt_  
    **or**
  - _pip install requests_
  - _pip install rich_ 
  - _pip install fuzzywuzzy_

- **Download the list of cities** from openweathermap to allow for fuzzy matching your input when their API doesn't like what you entered!
  - http://bulk.openweathermap.org/sample/city.list.json.gz _(3.8mb download, 40mb when unzipped)_

- _(Optional) For faster fuzzy matching based on C++, install the following:_
  - _pip install python-Levenshtein_

# TODO ->  
- Have a _setup.py_ do all of this for you instead.
- Better visualization of upcoming forecast differences.
- Implement as a live website and skip all this mess.