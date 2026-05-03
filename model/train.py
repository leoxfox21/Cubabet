import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

FILE = "data/dataset.csv"
MODEL_FILE = "data/model.json"

def train():

    df = pd.read_csv(FILE)

    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2
    )

    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1
    )

    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print("Accuracy:", accuracy)

    model.save_model(MODEL_FILE)
