from datetime import datetime
from model.predict import predict


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


# 🔹 Movimiento de cuota
def get_line_movement(history, match_name):
    data = history.get(match_name, {}).get("over25", [])

    if len(data) < 2:
        return 0

    first = data[0]["odds"]
    last = data[-1]["odds"]

    return first - last  # positivo = baja cuota


# 🔹 ANALISIS PRINCIPAL
def analyze_match(match, history, home_stats, away_stats):
    picks = []

    match_name = f'{match["home_team"]} vs {match["away_team"]}'

    for bookmaker in match.get("bookmakers", []):
        for market in bookmaker.get("markets", []):

            if market["key"] != "totals":
                continue

            for outcome in market["outcomes"]:

                if outcome["name"] == "Over" and outcome["point"] == 2.5:

                    odds = outcome["price"]

                    # guardar historial
                    history = track_odds(history, match_name, odds)

                    # movement
                    movement = get_line_movement(history, match_name)

                    # modelo IA
                    prob_model = predict(
                        home_stats,
                        away_stats,
                        odds,
                        movement
                    )

                    # value
                    value = calculate_value(prob_model, odds)

                    # score final
                    score = value + (movement * 0.1)

                    # filtros
                    if value > 0.05 and movement > 0:
                        picks.append({
                            "match": match_name,
                            "odds": odds,
                            "prob": prob_model,
                            "value": value,
                            "movement": movement,
                            "score": score
                        })

    return picks, history
