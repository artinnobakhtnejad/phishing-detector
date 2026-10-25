import joblib
import pandas as pd
from features import extract_features, get_domain

# Load the trained model once
model = joblib.load("models/phishing_model.joblib")

# Well-known domains we trust (a real system would use thousands)
TRUSTED_DOMAINS = [
    "google.com", "youtube.com", "github.com", "amazon.com", "amazon.ca",
    "microsoft.com", "apple.com", "paypal.com", "facebook.com", "instagram.com",
    "linkedin.com", "wikipedia.org", "netflix.com", "yorku.ca",
]


def is_trusted(domain):
    """True if the domain is a trusted domain or one of its subdomains."""
    return any(domain == trusted or domain.endswith("." + trusted) for trusted in TRUSTED_DOMAINS)


def check_url(url):
    """Return (verdict, chance it is safe, reason)."""
    domain = get_domain(url)

    # Layer 1: the allowlist
    if is_trusted(domain):
        return "SAFE", 1.0, "trusted domain"

    # Layer 2: the ML model
    features = pd.DataFrame([extract_features(url)])
    safe_chance = model.predict_proba(features)[0, 1]
    verdict = "SAFE" if safe_chance >= 0.5 else "PHISHING"
    return verdict, safe_chance, "model"


# Test it
if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",
        "https://accounts.google.com/signin",
        "https://github.com/login",
        "https://www.amazon.ca/gp/your-account/order-history",
        "http://paypal-verify-account.xyz/login",
        "https://secure-login-apple.com.verify-id.info/account",
        "http://192.168.0.1/bank/update",
        "https://google.com.account-check.info/login",
    ]
    for url in test_urls:
        verdict, chance, reason = check_url(url)
        print(f"{verdict:9} ({chance:.0%} safe, {reason})  {url}")