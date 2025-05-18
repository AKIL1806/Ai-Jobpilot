# main.py

from app.fetch_jobs import fetch_remote_jobs
import json
from pathlib import Path

def main():
    jobs = fetch_remote_jobs()

    print(f"Found {len(jobs)} matching jobs:\n")
    for job in jobs:
        print(f"{job['position']} at {job['company']} - {job['url']}")

    # Optional: save to file
    Path("data/jobs.json").write_text(json.dumps(jobs, indent=2))

if __name__ == "__main__":
    main()
# This script fetches remote jobs from RemoteOK, filters them based on keywords,
# and prints the results. It also saves the filtered jobs to a JSON file.