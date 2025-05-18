# app/fetch_jobs.py
import requests
from app.config import PREFERRED_KEYWORDS, EXCLUDED_KEYWORDS

def fetch_remote_jobs():
    url = "https://remoteok.io/api"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error fetching jobs:", response.status_code)
        return []

    jobs = response.json()[1:]  # Skip metadata

    def is_match(job):
        title = job.get("position", "").lower()
        return (
            any(kw in title for kw in PREFERRED_KEYWORDS) and
            not any(ex in title for ex in EXCLUDED_KEYWORDS)
        )

    filtered = [job for job in jobs if is_match(job)]
    return filtered
