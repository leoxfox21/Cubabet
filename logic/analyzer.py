from datetime import datetime
from model.predict import predict


# -----------------------------
# VALUE CALC
# -----------------------------

def calculate_value(prob, odds):
    return (prob * odds) - 1


# -----------------------------
# TRACK ODDS
# -----------------------------

def track_odds(history, match_name, odds, match_date=None, match_time=None):

    now = datetime.utcnow().isoformat()

    if match_name not in history:
        history[match_name] = {"over25": []}

    history[match_name]["over25"].append({
        "time": now,
        "odds": odds
    })

    if match_date or match_time:
        history[match_name]["meta"] = {
            "date": match_date,
            "time": match_time
        }

    return history


# -----------------------------
# LINE MOVEMENT
# -----------------------------

def get_line_movement(history, match_name):

    data = history.get(match_name, {}).get("over25", [])

    if len(data) < 2:
        return 0

    first = data[0]["odds"]
    last = data[-1]["odds"]

    return first - last


# -----------------------------
# ANALYZER MAIN
# -----------------------------

def analyze_match(match, history, home_stats, away_stats):

    picks = []

    match_name = f"{match['home_team']} vs {match['away_team']}"

    for bookmaker in match.get("bookmakers", []):
        for market in bookmaker.get("markets", []):

            if market["key"] != "totals":
                continue

            for outcome in market.get("outcomes", []):

                if outcome["name"] == "Over" and outcome["point"] == 2.5:

                    odds = outcome["price"]

                    history = track_odds(history, match_name, odds)

                    movement = get_line_movement(history, match_name)

                    prob_model = predict(
                        home_stats,
                        away_stats,
                        odds,
                        movement
                    )

                    value = calculate_value(prob_model, odds)

                    score = value + (movement * 0.15)

                    # 🔥 FILTER INTELIGENTE
                    if (
                        prob_model >= 0.58 and
                        value >= 0.06 and
                        movement > 0 and
                        score >= 0.10
                    ):
                        picks.append({
                            "match": match_name,
                            "odds": odds,
                            "prob": prob_model,
                            "value": value,
                            "movement": movement,
                            "score": score
                        })

    return picks, history
