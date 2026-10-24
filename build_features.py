import pandas as pd
from features import extract_features

# Load the dataset
df = pd.read_csv("data/PhiUSIIL_Phishing_URL_Dataset.csv")
print("Extracting features from", len(df), "URLs...")

# Run extract_features on every URL
feature_dicts = df["URL"].apply(extract_features)

# Turn the list of dictionaries into a table
X = pd.DataFrame(feature_dicts.tolist())
X["label"] = df["label"]

print("\nFirst 5 rows:")
print(X.head())

# Compare averages: phishing (0) vs safe (1)
print("\nAverage of each feature by label:")
print(X.groupby("label").mean().round(2).T)

# Save the table for Phase 4
X.to_csv("data/features.csv", index=False)
print("\nSaved to data/features.csv")