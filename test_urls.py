import joblib
import pandas as pd
from features import extract_features

# Load the saved model
model = joblib.load("models/phishing_model.joblib")

# URLs to test (do NOT open the fake ones in a browser)
test_urls = [
    # Real, safe websites
    "https://www.google.com",
    "https://accounts.google.com/signin",
    "https://github.com/login",
    "https://www.amazon.ca/gp/your-account/order-history",
    # Made-up phishing-style URLs
    "http://paypal-verify-account.xyz/login",
    "https://secure-login-apple.com.verify-id.info/account",
    "http://192.168.0.1/bank/update",
]

# Turn the URLs into features, then predict
X = pd.DataFrame([extract_features(url) for url in test_urls])
predictions = model.predict(X)
safe_chance = model.predict_proba(X)[:, 1]

for url, pred, chance in zip(test_urls, predictions, safe_chance):
    verdict = "SAFE" if pred == 1 else "PHISHING"
    print(f"{verdict:9} ({chance:.0%} safe)  {url}")