import requests
from config import FOOTBALL_API_KEY

def get_team_stats(team_id):
    url = f"https://api.football-data.org/v4/teams/{team_id}/matches?status=FINISHED"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}

    res = requests.get(url, headers=headers)
    data = res.json()

    goals = []

    for match in data.get("matches", [])[:5]:
        home = match["score"]["fullTime"]["home"]
        away = match["score"]["fullTime"]["away"]

        if home is not None and away is not None:
            goals.append(home + away)

    if not goals:
        return 0

    return sum(goals) / len(goals)
