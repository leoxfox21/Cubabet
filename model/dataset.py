import csv
import os

FILE = "data/dataset.csv"


def save_example(home_stats, away_stats, result_goals, odds, movement):

    home_attack = home_stats["attack"]
    home_defense = home_stats["defense"]
    away_attack = away_stats["attack"]
    away_defense = away_stats["defense"]

    attack_diff = home_attack - away_defense
    away_diff = away_attack - home_defense

    power = home_attack + away_attack
    weakness = home_defense + away_defense

    row = [
        home_attack,
        home_defense,
        away_attack,
        away_defense,
        attack_diff,
        away_diff,
        power,
        weakness,
        odds,
        movement,
        result_goals > 2.5
    ]

    file_exists = os.path.isfile(FILE)

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "home_attack",
                "home_defense",
                "away_attack",
                "away_defense",
                "attack_diff",
                "away_diff",
                "power",
                "weakness",
                "odds",
                "movement",
                "target"
            ])

        writer.writerow(row)
