import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score

# Load the features and split them EXACTLY like train_model.py did
data = pd.read_csv("data/features.csv")
X = data.drop(columns=["label"])
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Load the trained model and get its "chance it's safe" for each test URL
model = joblib.load("models/phishing_model.joblib")
safe_chance = model.predict_proba(X_test)[:, 1]

print("Threshold | Phishing caught | Precision | Safe sites blocked")
for threshold in [0.5, 0.6, 0.7, 0.8, 0.9]:
    predictions = (safe_chance >= threshold).astype(int)
    recall = recall_score(y_test, predictions, pos_label=0)
    precision = precision_score(y_test, predictions, pos_label=0)
    blocked = ((predictions == 0) & (y_test == 1)).sum()
    print(f"{threshold:9} | {recall:15.1%} | {precision:9.1%} | {blocked:18}")