import requests

URL = "https://api.openweathermap.org/data/2.5/weather"
TEST_URL = "https://httpbin.org/get"


def request_weather(_config):
    args = {
        'lat': _config["lat"],
        'lon': _config["lon"],
        "units": _config["units"],
        "mode": "json",  # must always be json
        "lang": _config["lang"],
        "appid": _config["appid"]
    }
    return requests.get(URL, args).text


def get_weather_icon_code(_data):
    weather = _data["weather"]
    return weather[0]["icon"]