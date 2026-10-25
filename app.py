import streamlit as st
from features import extract_features, get_domain
from predict import check_url

# Must be the first Streamlit command: browser tab title, icon and layout
st.set_page_config(page_title="Phishing URL Detector", page_icon="🎣", layout="centered")

EXAMPLES = {
    "✅ GitHub login": "https://github.com/login",
    "🚩 Fake PayPal": "http://paypal-verify-account.xyz/login",
    "🚩 IP address": "http://192.168.0.1/bank/update",
}


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


def show_result(url):
    """Check a URL and display the result card."""
    verdict, safe_chance, reason = check_url(url)
    risk = float(1 - safe_chance)

    with st.container(border=True):
        if verdict == "PHISHING":
            st.error("🔴 **PHISHING**: do not enter any information on this site.")
        elif verdict == "SUSPICIOUS":
            st.warning("🟡 **SUSPICIOUS**: be careful with this link.")
        else:
            st.success("🟢 **SAFE**: no obvious warning signs.")

        st.progress(risk, text=f"Phishing risk: {risk:.0%}")

        col1, col2 = st.columns(2)
        col1.metric("Domain checked", get_domain(url))
        col2.metric("Decided by", "Trusted list" if reason == "trusted domain" else "ML model")

        if reason == "trusted domain":
            st.write("✅ This website is on our list of trusted domains.")
        else:
            signs = warning_signs(url)
            if signs:
                st.markdown("**Warning signs found:**")
                for sign in signs:
                    st.markdown(f"- {sign}")
            else:
                st.write("No obvious warning signs found in the domain.")


# ---------- Sidebar ----------
with st.sidebar:
    st.header("🎣 About")
    st.write("Built by **Artin Nobakhtnejad**, Computer Science student at York University.")
    st.write("It combines a list of trusted websites with a Random Forest model trained on 235,000 real URLs.")
    st.markdown("[View the code on GitHub](https://github.com/artinnobakhtnejad/phishing-detector)")
    st.caption("A student project for learning purposes.")

# ---------- Main page ----------
st.title("🎣 Phishing URL Detector")
st.markdown("##### Is that link safe? Paste it below and find out in a second.")

# Remember the URL between clicks
if "url" not in st.session_state:
    st.session_state.url = ""

st.write("**Try an example:**")
example_clicked = False
cols = st.columns(len(EXAMPLES))
for col, (label, example_url) in zip(cols, EXAMPLES.items()):
    if col.button(label):
        st.session_state.url = example_url
        example_clicked = True

st.text_input("URL to check", key="url", placeholder="https://example.com/login")
check_clicked = st.button("Check URL", type="primary")

if check_clicked or example_clicked:
    url = st.session_state.url.strip()
    if not url:
        st.warning("Please paste a URL first.")
    else:
        if "://" not in url:
            url = "https://" + url
        show_result(url)

with st.expander("ℹ️ How does it work?"):
    st.markdown(
        """
1. **Trusted list:** well-known sites like google.com and github.com are recognised instantly.
2. **Machine learning:** for every other link, a Random Forest model looks at 12 clues in the domain, such as how random the name looks, whether it uses a free hosting platform, or a suspicious ending like `.xyz`.
3. **Verdict:** below 50% chance of being safe is **phishing**, 50–70% is **suspicious**, and above 70% is **safe**.

The model reaches 83.5% accuracy on 47,000 unseen URLs. It cannot see the path of a URL, so phishing pages hidden on hacked real websites can slip through.
"""
    )

st.caption("⚠️ This tool can make mistakes. Always double-check links before entering passwords.")