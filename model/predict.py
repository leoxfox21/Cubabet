import xgboost as xgb
import numpy as np
import os

MODEL_FILE = "data/model.json"

model = xgb.XGBClassifier()

if os.path.exists(MODEL_FILE):
    model.load_model(MODEL_FILE)
else:
    model = None


def predict(home_stats, away_stats, odds, movement):

    if model is None:
        return 0.55

    home_attack = home_stats["attack"]
    home_defense = home_stats["defense"]
    away_attack = away_stats["attack"]
    away_defense = away_stats["defense"]

    attack_diff = home_attack - away_defense
    away_diff = away_attack - home_defense

    power = home_attack + away_attack
    weakness = home_defense + away_defense

    X = np.array([[
        home_attack,
        home_defense,
        away_attack,
        away_defense,
        attack_diff,
        away_diff,
        power,
        weakness,
        odds,
        movement
    ]])

    return model.predict_proba(X)[0][1]
