import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('WEATHER_API_KEY')

def get_weather(city, lang="ru",units='metric'):
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang={lang}&units={units}",timeout=10)
    data = json.loads(r.text)
    print(data)
    if "cod" in data and data["cod"] == "500":
        return "Невозможно подключится к серверу"
    description = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    visibility = data["visibility"]
    wind_speed = data["wind"]["speed"]
    clouds = data["clouds"]["all"]
    if "rain" in data:
        rain = str(data["rain"]["1h"]) + " милиметров за последний час"
    else:
        rain = "Дождя нет"
    
    if "snow" in data:
        snow = str(data["snow"]["1h"]) + " милиметров за последний час"
    else:
        snow = "Снега нет"

    str_description = f"Описание погоды: {description}\n"
    str_temp = f"Температура на улице: {temp}, ощющается как: {feels_like}\n"
    str_humidity = f"Влажность: {humidity}%\n"
    str_visibility = f"Видимость: {visibility} метров\n"
    str_wind_speed = f"Скорость ветра: {wind_speed}\n"
    str_clouds = f"Облачность: {clouds}%\n"
    str_rain = f"Дождь: {rain}\n"
    str_snow = f"Снег: {snow}"

    result = str_description + str_temp + str_humidity + str_visibility + str_wind_speed + str_clouds + str_rain + str_snow
    return result

if __name__ == "__main__":
    print(get_weather("Ревда"))