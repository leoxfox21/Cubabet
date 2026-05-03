from datetime import datetime

def implied_prob(odds):
    return 1 / odds


def calculate_value(prob, odds):
    return (prob * odds) - 1


# 🔹 Guardar historial de cuotas
def track_odds(history, match_name, odds):
    now = datetime.utcnow().isoformat()

    if match_name not in history:
        history[match_name] = {"over25": []}

    history[match_name]["over25"].append({
        "time": now,
        "odds": odds
    })

    return history


# 🔹 Detectar movimiento de cuotas
def get_line_movement(history, match_name):
    data = history.get(match_name, {}).get("over25", [])

    if len(data) < 2:
        return 0

    first = data[0]["odds"]
    last = data[-1]["odds"]

    return first - last  # positivo = cuota bajó


# 🔹 Analizar partido completo
def analyze_match(match, history, stats_home, stats_away):
    picks = []

    match_name = f'{match["home_team"]} vs {match["away_team"]}'
    expected_goals = (stats_home + stats_away) / 2

    for bookmaker in match.get("bookmakers", []):
        for market in bookmaker.get("markets", []):
            if market["key"] == "totals":

                for outcome in market["outcomes"]:
                    if outcome["name"] == "Over" and outcome["point"] == 2.5:
                        odds = outcome["price"]

                        # 🔹 guardar historial
                        history = track_odds(history, match_name, odds)

                        # 🔹 modelo simple
                        prob_model = min(0.75, expected_goals / 4)

                        value = calculate_value(prob_model, odds)

                        # 🔹 movimiento de cuota
                        movement = get_line_movement(history, match_name)

                        # 🔹 score combinado
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
