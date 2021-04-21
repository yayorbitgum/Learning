import unittest
from WeatherGet import determine_state_code
from WeatherGet import wind_degrees_to_direction
from WeatherGet import request_weather_api
from WeatherGet import WeatherAPIData
from WeatherGet import save_json
from WeatherGet import open_json
from config import my_key


class WeatherGetTests(unittest.TestCase):
    """Tests for functions and methods in WeatherGet.py."""

    def test_wind_direction(self):
        """Ensure bisecting is setup correctly and returns proper direction."""
        tests = ((90, "East"),
                 (10, "North"),
                 (358, "North"),
                 (182, "South"),
                 (270, "West"),
                 (300, "Northwest"),
                 (285, "Northwest"),
                 (45, "Northeast"),
                 (135, "Southeast"),
                 (225, "Southwest"),
                 )

        for degrees, expected_direction in tests:
            result = wind_degrees_to_direction(degrees)
            self.assertEqual(expected_direction, result, f"input degrees: {degrees}")

    def test_state_code(self):
        """Ensure city_id returned by API request also matches up to city.list.json."""
        tests = ((5345990, "CA"),
                 (5346462, "CA"),
                 (5528182, "TX"),
                 (5528274, "TX"),
                 (4154937, "FL"),
                 (6357720, ""),
                 (2975244, ""),
                 (0, ""),
                 ("wowee", ""),
                 )

        for test in tests:
            city_id = test[0]
            state_code = test[1]
            result = determine_state_code('city.list.json', city_id)
            self.assertEqual(state_code, result, f"input city_id: {city_id}")

    def test_api_data_responses(self):
        """
        Test for differences in data received depending on if a request is
        made to openweather with a city name, or with a city ID.
        """
        cities = (("Oklahoma City", 4544349),
                  ("Del City", 4534934),
                  ("New York City", 5128581),
                  ("Los Angeles", 5368361),
                  ("Loomis", 5368233)
                  )

        for city in cities:
            city_name = city[0]
            city_id = city[1]
            by_name = request_weather_api(my_key, city_name)
            by_city_id = request_weather_api(my_key, city_name, city_id)
            # Assert both types of requests are accepted.
            with self.subTest(f"Check status codes."):
                self.assertEqual(by_name[0].status_code, by_city_id[0].status_code)

            # Save requests so we can examine WeatherAPIData class.
            name_path = "json_files/by_name.json"
            id_path = "json_files/by_city_id.json"
            save_json(by_name[0], name_path)
            save_json(by_city_id[0], id_path)
            n_api = WeatherAPIData(open_json(name_path), 0)
            id_api = WeatherAPIData(open_json(id_path), 0)

            # Assert relevant api data matches.
            for n_data, id_data in zip(n_api, id_api):
                with self.subTest("API data points test."):
                    self.assertEqual(n_data, id_data,
                                     f"{n_data[0]} mismatch for {city_name}."
                                     f" (id = {city_id})\n"
                                     f"By name request returns {n_data[1]}, but"
                                     f" by city id request returns {id_data[1]}.")
            # Through these tests I was able to determine openweathermap's api
            # does not return population data if you request directly by city_id.
            # These are made with different API calls.
            # "?id=" in the request URL for city ID, otherwise you use "?q=" for
            # querying by location name. Are these returning two different
            # json files?


if __name__ == '__main__':
    unittest.main()
