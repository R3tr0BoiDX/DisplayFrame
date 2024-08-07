import json
import requests

URL = "https://api.openweathermap.org/data/2.5/weather"
TIMEOUT = 10


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
    return requests.get(URL, args, timeout=TIMEOUT).text


def get_weather_code(_data):
    weather = _data["weather"]
    return weather[0]["icon"]


def get_sunset_and_rise(_data):
    sys = _data["sys"]
    sunrise = int(sys["sunrise"])
    sunset = int(sys["sunset"])
    return sunrise, sunset


def get_weather_and_sun():
    json_raw = request_weather(read_config())
    data = json.loads(json_raw)
    weather_code = get_weather_code(data)
    sun = get_sunset_and_rise(data)
    return weather_code, sun
