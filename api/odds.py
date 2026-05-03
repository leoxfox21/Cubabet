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
    return res.json()
