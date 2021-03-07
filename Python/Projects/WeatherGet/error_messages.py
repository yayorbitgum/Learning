message_forbidden = "Your key was rejected with a 401 response code (Unauthorized)." \
                    "Did you setup your API key properly?\n " \
                    "Double check at --> https://openweathermap.org/api " \
                    "for the 'Current Weather Data'. Click Subscribe and choose " \
                    "the free option.\n" \
                    "Then, check for your API key at --> https://home.openweathermap.org/api_keys\n" \
                    "Enter that key in config.py and try again."

missing_api_exception = Exception('You need an API key from openweathermap.org to grab current weather data.\n'
                                  'Register, generate a key, and save that key as a string in config.py.\n'
                                  'You can find your key(s) here --> https://home.openweathermap.org/api_keys')