# 🎣 Phishing URL Detector

A machine learning web app that checks whether a URL looks safe or like a phishing attempt, and explains why.

**🔗 Live demo:** *coming soon*

## What it does

Paste any link and the app returns one of three verdicts:

- 🔴 **PHISHING**: high risk, do not enter any information
- 🟡 **SUSPICIOUS**: uncertain, be careful
- 🟢 **SAFE**: no obvious warning signs

It also lists the warning signs it found, such as a free hosting platform, a random-looking domain name, or a suspicious domain ending like `.xyz`.

## How it works

The checker uses two layers, like real security tools:

1. **Allowlist**: well-known domains (google.com, github.com, …) and their subdomains are trusted.
2. **Machine learning model**: a Random Forest classifier judges every other URL from 12 features of its domain.

| Feature | What it catches |
|---|---|
| `domain_entropy` | Randomly generated names like `hidok4f8zl` (Shannon entropy) |
| `uses_free_hosting` | Pages on firebaseapp.com, weeblysite.com, web.app, … |
| `suspicious_tld` | Domain endings often abused for phishing (.xyz, .tk, .gq, …) |
| `is_ip_address` | Bare IP addresses instead of a website name |
| `digit_ratio`, `num_digits` | Domains full of numbers |
| `num_dots`, `num_hyphens`, `domain_length`, `longest_part` | Long, deeply nested or hyphen-heavy domains |
| `has_suspicious_word` | Domain parts like `login`, `verify`, `account` |
| `has_at_symbol` | The `@` trick that hides the real destination |

## Results

Trained on 188,636 URLs and tested on 47,159 unseen URLs from the [PhiUSIIL Phishing URL Dataset](https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset).

| Model version | Accuracy | Phishing caught (recall) | Real-world test |
|---|---|---|---|
| 1. Full URL features | 99.5% | 99.0% | 4 of 7 correct |
| 2. Domain-only features | 81.0% | 61.0% | 6 of 7 correct |
| 3. Domain + entropy and security features (final) | 83.5% | 67.5% | 10 of 11 correct (with allowlist) |

### Why the 99.5% model was rejected

The first model scored 99.5%, but when tested on real URLs it flagged GitHub login, Google sign-in and an Amazon order page as phishing.

The cause was **dataset bias**: almost every safe URL in the dataset is a bare homepage like `https://www.example.org`, and every one uses HTTPS. The model learned a shortcut ("homepage with HTTPS = safe") instead of real phishing patterns. Its top feature, `has_https`, carried 41% of its decisions.

I rebuilt the features to use only the domain, removed `www.` and `has_https`, and added security-focused features. Accuracy dropped to an honest 83.5%, but the model now works on real websites.

### Threshold tuning

| Threshold | Phishing caught | Safe sites wrongly blocked |
|---|---|---|
| 0.5 | 67.5% | 4.6% |
| 0.7 | 73.1% | 12.3% |
| 0.9 | 97.6% | 88% |

Catching more phishing always costs more false alarms. Instead of blocking every uncertain link, the app shows a **SUSPICIOUS** warning between 50% and 70%.

## Limitations

- **Hacked legitimate sites**: many phishing pages are hosted on real, compromised websites. Their domain looks normal and only the path reveals them, which this domain-based model cannot see.
- **Subdomains of unknown sites**: for example, `news.ycombinator.com` is wrongly flagged.
- **Small allowlist**: real tools use lists of the top million websites.
- **Explanations are simple rules**: the warning signs are approximate and can be misleading (long real-word domains can trigger the "random-looking" sign).

## Future improvements

- Train on legitimate URLs that include paths, so path features can be used fairly
- Use a large allowlist such as the Tranco top-sites list
- Add brand-impersonation detection (e.g. "paypal" in a domain that is not paypal.com)

## Tech stack

Python · pandas · scikit-learn · Streamlit · joblib

## Run it locally

```bash
git clone https://github.com/artinnobakhtnejad/phishing-detector.git
cd phishing-detector
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

To retrain the model, download the dataset from UCI into `data/`, then run `build_features.py` and `train_model.py`.

## Project structure

| File | Purpose |
|---|---|
| `features.py` | Turns a URL into numeric features |
| `build_features.py` | Builds the feature table for all URLs |
| `train_model.py` | Trains, evaluates and saves the model |
| `tune_threshold.py` | Compares decision thresholds |
| `predict.py` | Allowlist + model checker (`check_url`) |
| `app.py` | Streamlit web app |
| `explore_data.py`, `test_urls.py` | Data exploration and real-world tests |

## Dataset

Prasad, A. & Chandra, S. (2024). *PhiUSIIL Phishing URL Dataset*. UCI Machine Learning Repository.

## Author

**Artin Nobakhtnejad**, Computer Science student at York University
[LinkedIn](https://www.linkedin.com/in/artin-nobakhtnejad-15512a256)

*This is a student project for learning purposes. Always double-check links before entering passwords.*