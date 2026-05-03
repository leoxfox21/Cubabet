import json
from api.odds import get_odds
from api.stats import get_team_stats
from logic.analyzer import analyze_match
from bot.telegram import send_message

def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)


def main():
    odds = get_odds()
    history = load_data()

    all_picks = []

    for match in odds:
        # ⚠️ aquí necesitas mapear equipos a IDs reales
        home_stats = get_team_stats(1)
        away_stats = get_team_stats(2)

        picks = analyze_match(match, home_stats, away_stats)

        for pick in picks:
            msg = f"""
⚽ SERIE A PICK

{pick['match']}
Over 2.5

Odds: {pick['odds']}
xG: {round(pick['expected_goals'],2)}

Prob: {round(pick['prob']*100,1)}%
Value: {round(pick['value']*100,1)}%
"""
            send_message(msg)
            all_picks.append(pick)

    history.extend(all_picks)
    save_data(history)


if __name__ == "__main__":
    main()
