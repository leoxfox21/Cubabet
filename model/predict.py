import xgboost as xgb
import numpy as np

MODEL_FILE = "data/model.json"

model = xgb.XGBClassifier()
model.load_model(MODEL_FILE)


def predict(home_stats, away_stats, odds, movement):

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
