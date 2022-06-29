import json

import requests
from datetime import datetime

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


def get_current_time():
    now = datetime.now()
    return now.strftime("%H%M")


def read_config():
    with open('config.json') as f:
        return json.load(f)


def help_config():
    print("You need to config the config.json. You can use the config.example.json as starting point")
    print("See https://openweathermap.org/current for valid config entries")


if __name__ == '__main__':
    config = read_config()
    json_text = request_weather(config)
    data = json.loads(json_text)

    code = get_weather_icon_code(data)
    time = get_current_time()

    print(code)
    print(time)
