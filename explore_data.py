import pandas as pd

# Load the CSV file into a table (called a DataFrame)
df = pd.read_csv("data/PhiUSIIL_Phishing_URL_Dataset.csv")

# How big is it? (rows, columns)
print("Rows and columns:", df.shape)

# What are the column names?
print("\nColumns:")
print(df.columns.tolist())

# Show the first 10 URLs and their labels
print("\nFirst 10 rows:")
print(df[["URL", "label"]].head(10))

# How many of each label?
print("\nLabel counts:")
print(df["label"].value_counts())

# Show 10 phishing URLs (label 0)
print("\nPhishing examples:")
phishing = df[df["label"] == 0]
print(phishing["URL"].head(10).to_string())