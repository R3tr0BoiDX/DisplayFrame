import json
import requests

URL = "https://api.openweathermap.org/data/2.5/weather"
TEST_URL = "https://httpbin.org/get"


def read_config():
    with open('config.json') as f:
        return json.load(f)


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


def get_weather_code_from_json(_data):
    weather = _data["weather"]
    return weather[0]["icon"]


def get_weather_code():
    json_raw = request_weather(read_config())
    data = json.loads(json_raw)
    return get_weather_code_from_json(data)
