from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from features import get_domain
from predict import check_url, warning_signs

app = FastAPI(title="Phishing URL Detector API")


class URLRequest(BaseModel):
    url: str = Field(min_length=1, max_length=2000)


@app.post("/api/check")
def check(request: URLRequest):
    url = request.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="Please provide a URL.")
    if "://" not in url:
        url = "https://" + url

    verdict, safe_chance, reason = check_url(url)
    signs = [] if reason == "trusted domain" else warning_signs(url)

    return {
        "url": url,
        "domain": get_domain(url),
        "verdict": verdict,
        "risk": round(1 - float(safe_chance), 3),
        "decided_by": reason,
        "warning_signs": signs,
    }