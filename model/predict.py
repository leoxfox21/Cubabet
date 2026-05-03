import xgboost as xgb
import numpy as np
import os

MODEL_FILE = "data/model.json"

model = xgb.XGBClassifier()

if os.path.exists(MODEL_FILE):
    model.load_model(MODEL_FILE)
else:
    model = None  # fallback


def predict(home_stats, away_stats, odds, movement):

    if model is None:
        # fallback simple si no hay modelo
        return 0.55

    X = np.array([[
        home_stats["attack"],
        home_stats["defense"],
        away_stats["attack"],
        away_stats["defense"],
        odds,
        movement
    ]])

    prob = model.predict_proba(X)[0][1]

    return prob
