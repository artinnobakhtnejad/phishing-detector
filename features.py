from urllib.parse import urlparse

# Words attackers often put in phishing URLs
SUSPICIOUS_WORDS = ["login", "verify", "secure", "account", "update", "bank", "signin", "password"]


def extract_features(url):
    """Turn one URL into a dictionary of numbers."""
    parsed = urlparse(url)
    domain = parsed.netloc

    features = {
        "url_length": len(url),
        "num_dots": url.count("."),
        "num_digits": sum(c.isdigit() for c in url),
        "num_hyphens": url.count("-"),
        "has_https": 1 if parsed.scheme == "https" else 0,
        "has_at_symbol": 1 if "@" in url else 0,
        "domain_length": len(domain),
        "has_suspicious_word": 1 if any(word in url.lower() for word in SUSPICIOUS_WORDS) else 0,
    }
    return features


# Test it on one safe and one phishing URL
if __name__ == "__main__":
    test_urls = [
        "https://www.aap.org",
        "http://att-103731-107123.weeblysite.com/",
    ]
    for url in test_urls:
        print(url)
        print(extract_features(url))
        print()