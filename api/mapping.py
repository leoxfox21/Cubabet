import requests
from config import FOOTBALL_API_KEY

# cache en memoria
TEAM_CACHE = {}

def get_all_teams():
    url = "https://api.football-data.org/v4/competitions/SA/teams"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}

    res = requests.get(url, headers=headers)
    data = res.json()

    teams = []
    for t in data.get("teams", []):
        teams.append({
            "id": t["id"],
            "name": t["name"].lower()
        })

    return teams


def find_team_id(team_name):
    team_name = team_name.lower()

    if team_name in TEAM_CACHE:
        return TEAM_CACHE[team_name]

    teams = get_all_teams()

    best_match = None
    best_score = 0

    for team in teams:
        name = team["name"]

        # similitud simple
        score = similarity(team_name, name)

        if score > best_score:
            best_score = score
            best_match = team

    if best_match:
        TEAM_CACHE[team_name] = best_match["id"]
        return best_match["id"]

    return None


def similarity(a, b):
    a = set(a.split())
    b = set(b.split())

    return len(a & b) / max(len(a), len(b))
