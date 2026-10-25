import streamlit as st
from features import extract_features
from predict import check_url


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


st.title("🎣 Phishing URL Detector")
st.write("Paste a link to check whether it looks safe or like a phishing attempt.")

url = st.text_input("URL to check", placeholder="https://example.com/login")

if st.button("Check URL"):
    url = url.strip()
    if not url:
        st.warning("Please paste a URL first.")
    else:
        if "://" not in url:
            url = "https://" + url

        verdict, safe_chance, reason = check_url(url)
        risk = 1 - safe_chance

        if verdict == "PHISHING":
            st.error(f"🔴 PHISHING: {risk:.0%} phishing risk")
        elif verdict == "SUSPICIOUS":
            st.warning(f"🟡 SUSPICIOUS: {risk:.0%} phishing risk")
        else:
            st.success(f"🟢 SAFE: {risk:.0%} phishing risk")

        if reason == "trusted domain":
            st.write("✅ This website is on our list of trusted domains.")
        else:
            signs = warning_signs(url)
            if signs:
                st.write("**Warning signs found:**")
                for sign in signs:
                    st.write(f"- {sign}")
            else:
                st.write("No obvious warning signs found in the domain.")

        st.caption("This is a student project. Always double-check links before entering passwords.")