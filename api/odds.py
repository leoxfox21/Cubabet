import requests
from config import ODDS_API_KEY

URL = "https://api.the-odds-api.com/v4/sports/soccer_italy_serie_a/odds"

def get_odds():

    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "eu",
        "markets": "totals"
    }

    res = requests.get(URL, params=params)

    # 🔥 validar respuesta
    if res.status_code != 200:
        print("ERROR ODDS API:", res.text)
        return []

    try:
        data = res.json()
    except:
        print("ERROR parsing JSON:", res.text)
        return []

    # 🔥 validar tipo
    if not isinstance(data, list):
        print("Unexpected format:", type(data))
        return []

    return data
