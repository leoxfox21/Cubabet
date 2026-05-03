import json
from api.odds import get_odds
from api.stats import get_team_stats, get_last_match_goals
from api.mapping import find_team_id
from logic.analyzer import analyze_match, get_line_movement
from bot.telegram import send_message
from model.dataset import save_example


def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except:
        return {}


def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)


def extract_odds(match):
    for bookmaker in match.get("bookmakers", []):
        for market in bookmaker.get("markets", []):
            if market["key"] == "totals":
                for outcome in market["outcomes"]:
                    if outcome["name"] == "Over" and outcome["point"] == 2.5:
                        return outcome["price"]
    return None


def main():
    odds_data = get_odds()
    history = load_data()

    for match in odds_data:

        home_name = match["home_team"]
        away_name = match["away_team"]

        home_id = find_team_id(home_name)
        away_id = find_team_id(away_name)

        if not home_id or not away_id:
            continue

        # stats reales
        home_stats = get_team_stats(home_id)
        away_stats = get_team_stats(away_id)

        # análisis (esto ya actualiza history internamente)
        picks, history = analyze_match(
            match,
            history,
            home_stats,
            away_stats
        )

        match_name = f"{home_name} vs {away_name}"

        # movement para dataset
        movement = get_line_movement(history, match_name)

        # odds actuales
        odds_value = extract_odds(match)

        # resultado real
        result_goals = get_last_match_goals(home_id)

        # guardar dataset
        if result_goals is not None and odds_value is not None:
            save_example(
                home_stats,
                away_stats,
                result_goals,
                odds_value,
                movement
            )

        # enviar picks
        for pick in picks:
            msg = f"""
⚽ SERIE A PICK

{pick['match']}
Over 2.5

Odds: {pick['odds']}

Prob: {round(pick['prob']*100,1)}%
Value: {round(pick['value']*100,1)}%

Movement: {round(pick['movement'],3)}
Score: {round(pick['score'],3)}
"""
            send_message(msg)

    save_data(history)


if __name__ == "__main__":
    main()
