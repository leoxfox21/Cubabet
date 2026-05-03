from datetime import datetime

def calculate_value(prob, odds):
    return (prob * odds) - 1


# tracking odds
def track_odds(history, match_name, odds):
    now = datetime.utcnow().isoformat()

    if match_name not in history:
        history[match_name] = {"over25": []}

    history[match_name]["over25"].append({
        "time": now,
        "odds": odds
    })

    return history


def get_line_movement(history, match_name):
    data = history.get(match_name, {}).get("over25", [])

    if len(data) < 2:
        return 0

    return data[0]["odds"] - data[-1]["odds"]


# 🔥 NUEVO MODELO
def predict_goals(home_stats, away_stats):
    home_attack = home_stats["attack"]
    home_defense = home_stats["defense"]

    away_attack = away_stats["attack"]
    away_defense = away_stats["defense"]

    # fórmula mejorada
    expected_home_goals = (home_attack + away_defense) / 2
    expected_away_goals = (away_attack + home_defense) / 2

    total_goals = expected_home_goals + expected_away_goals

    return total_goals


def goal_probability(expected_goals):
    # aproximación simple mejorada
    if expected_goals >= 3:
        return 0.70
    elif expected_goals >= 2.5:
        return 0.60
    elif expected_goals >= 2:
        return 0.52
    elif expected_goals >= 1.5:
        return 0.45
    else:
        return 0.35


def analyze_match(match, history, home_stats, away_stats):
    picks = []

    match_name = f'{match["home_team"]} vs {match["away_team"]}'

    expected_goals = predict_goals(home_stats, away_stats)
    prob_model = goal_probability(expected_goals)

    for bookmaker in match.get("bookmakers", []):
        for market in bookmaker.get("markets", []):
            if market["key"] == "totals":

                for outcome in market["outcomes"]:
                    if outcome["name"] == "Over" and outcome["point"] == 2.5:
                        odds = outcome["price"]

                        history = track_odds(history, match_name, odds)

                        value = calculate_value(prob_model, odds)
                        movement = get_line_movement(history, match_name)

                        score = value + (movement * 0.1)

                        if value > 0.05 and movement > 0 and expected_goals > 2:
                            picks.append({
                                "match": match_name,
                                "odds": odds,
                                "expected_goals": expected_goals,
                                "prob": prob_model,
                                "value": value,
                                "movement": movement,
                                "score": score
                            })

    return picks, history
