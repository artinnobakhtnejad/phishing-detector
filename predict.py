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


def warning_signs(url):
    """Return a list of human-readable red flags found in the URL."""
    f = extract_features(url)
    signs = []
    if f["is_ip_address"]:
        signs.append("Uses an IP address instead of a website name")
    if f["uses_free_hosting"]:
        signs.append("Hosted on a free platform that attackers often abuse")
    if f["suspicious_tld"]:
        signs.append("Uses a domain ending (like .xyz) common in phishing")
    if f["has_suspicious_word"]:
        signs.append("Domain contains words like 'login', 'verify' or 'account'")
    if f["has_at_symbol"]:
        signs.append("Contains an @ symbol, a trick to hide the real destination")
    if f["digit_ratio"] > 0.2:
        signs.append("Domain name is full of numbers")
    if f["domain_entropy"] > 3.8:
        signs.append("Domain name looks randomly generated")
    if f["num_dots"] >= 3:
        signs.append("Many subdomains, a trick to look like a real brand")
    if f["num_hyphens"] >= 2:
        signs.append("Several hyphens in the domain name")
    return signs

def check_url(url):
    """Return (verdict, chance it is safe, reason)."""
    domain = get_domain(url)

    # Layer 1: the allowlist
    if is_trusted(domain):
        return "SAFE", 1.0, "trusted domain"

    # Layer 2: the ML model
    features = pd.DataFrame([extract_features(url)])
    safe_chance = model.predict_proba(features)[0, 1]
    if safe_chance < 0.5:
        verdict = "PHISHING"
    elif safe_chance < 0.7:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SAFE"
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
        "https://www.cbc.ca/news",
        "https://news.ycombinator.com",
        "https://www.reddit.com/r/learnpython",
    ]
    for url in test_urls:
        verdict, chance, reason = check_url(url)
        print(f"{verdict:10} ({chance:.0%} safe, {reason})  {url}")