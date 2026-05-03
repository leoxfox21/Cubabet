def implied_prob(odds):
    return 1 / odds


def calculate_value(prob, odds):
    return (prob * odds) - 1


def analyze_match(match, stats_home, stats_away):
    picks = []

    expected_goals = (stats_home + stats_away) / 2

    for bookmaker in match["bookmakers"]:
        for market in bookmaker["markets"]:
            if market["key"] == "totals":

                for outcome in market["outcomes"]:
                    if outcome["name"] == "Over" and outcome["point"] == 2.5:
                        odds = outcome["price"]

                        # modelo simple
                        prob_model = min(0.75, expected_goals / 4)

                        value = calculate_value(prob_model, odds)

                        if value > 0.05 and expected_goals > 2:
                            picks.append({
                                "match": f'{match["home_team"]} vs {match["away_team"]}',
                                "odds": odds,
                                "expected_goals": expected_goals,
                                "prob": prob_model,
                                "value": value
                            })

    return picks
