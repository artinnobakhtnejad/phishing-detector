import math
import re
from collections import Counter
from urllib.parse import urlparse


# Words attackers often put in phishing domains
SUSPICIOUS_WORDS = ["login", "verify", "secure", "account", "update", "bank", "signin", "password"]

# Free hosting platforms attackers often abuse
FREE_HOSTS = [
    "firebaseapp.com", "web.app", "weebly.com", "weeblysite.com", "wixsite.com",
    "000webhostapp.com", "netlify.app", "vercel.app", "pages.dev", "github.io",
    "herokuapp.com", "glitch.me", "ipfs.io", "lima-city.de", "blogspot.com",
]

# Top-level domains (the last part, like .com) often used for phishing
SUSPICIOUS_TLDS = ["xyz", "top", "tk", "ml", "ga", "cf", "gq", "icu", "buzz", "click"]

# Matches an IP address like 192.168.0.1
IP_PATTERN = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")

def entropy(text):
    """Measure how random a string looks (higher = more random)."""
    if not text:
        return 0
    counts = Counter(text)
    total = len(text)
    return -sum((n / total) * math.log2(n / total) for n in counts.values())



def get_domain(url):
    """Return just the domain, like 'accounts.google.com'."""
    domain = urlparse(url).netloc.lower()
    domain = domain.split("@")[-1]  # browsers ignore anything before @
    domain = domain.split(":")[0]   # remove a port like :8080
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def extract_features(url):
    """Turn one URL into numbers, using only its domain."""
    domain = get_domain(url)
    tld = domain.split(".")[-1]
    parts = re.split(r"[.-]", domain)

    features = {
        "domain_length": len(domain),
        "num_dots": domain.count("."),
        "num_digits": sum(c.isdigit() for c in domain),
        "num_hyphens": domain.count("-"),
        "domain_entropy": round(entropy(domain), 3),
        "longest_part": max(len(part) for part in parts),
        "digit_ratio": round(sum(c.isdigit() for c in domain) / max(len(domain), 1), 3),
        "is_ip_address": 1 if IP_PATTERN.match(domain) else 0,
        "uses_free_hosting": 1 if any(domain.endswith(host) for host in FREE_HOSTS) else 0,
        "suspicious_tld": 1 if tld in SUSPICIOUS_TLDS else 0,
        "has_suspicious_word": 1 if any(part in SUSPICIOUS_WORDS for part in parts) else 0,
        "has_at_symbol": 1 if "@" in url else 0,
    }
    return features


# Test it on a few URLs
if __name__ == "__main__":
    test_urls = [
        "https://www.aap.org",
        "https://accounts.google.com/signin",
        "http://att-103731-107123.weeblysite.com/",
    ]
    for url in test_urls:
        print(url, "->", get_domain(url))
        print(extract_features(url))
        print()