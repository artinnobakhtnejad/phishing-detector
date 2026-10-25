import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the features table from Phase 3
data = pd.read_csv("data/features.csv")

# X = the features (inputs), y = the label (the answer)
X = data.drop(columns=["label"])
y = data["label"]

# Split: 80% for training, 20% kept hidden for testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

# Create and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Test it on URLs it has never seen
predictions = model.predict(X_test)

print("\nAccuracy:", round(accuracy_score(y_test, predictions), 4))

print("\nConfusion matrix:")
print(confusion_matrix(y_test, predictions))

print("\nDetailed report:")
print(classification_report(y_test, predictions, target_names=["phishing", "safe"]))

# Which features did the model rely on most?
importances = pd.Series(model.feature_importances_, index=X.columns)
print("\nFeature importance:")
print(importances.sort_values(ascending=False).round(3))