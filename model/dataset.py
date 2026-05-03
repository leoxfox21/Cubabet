import csv
import os

FILE = "data/dataset.csv"

def save_example(home_stats, away_stats, result_goals):

    row = [
        home_stats["attack"],
        home_stats["defense"],
        away_stats["attack"],
        away_stats["defense"],
        result_goals > 2.5  # target
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
                "target"
            ])

        writer.writerow(row)
