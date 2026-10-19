import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('EXCHANGE_API_KEY')

def get_rate(api_key, base_currency):
    r = requests.get(f"https://openexchangerates.org/api/latest.json/?app_id={api_key}&base=USD")
    data = r.json()
    return data["rates"]


def convert(amount, from_,to,api_key=api_key):
    rates = get_rate(api_key,from_)
    if to in rates:
        rate = rates[to]
        converted = amount*rate
        return round(converted,3),to
    else:
        return None
if __name__ == "__main__":
    print(convert(211,"USD","BTC",api_key))