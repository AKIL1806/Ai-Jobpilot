import requests
from app.config import PREFERRED_KEYWORDS, EXCLUDED_KEYWORDS

PREFERRED_LOCATIONS = ['chennai', 'bangalore']

def filter_jobs_by_location(jobs, preferred_locations):
    filtered = []
    for job in jobs:
        location = job.get('location', '') or job.get('tags', [])
        # location can be string or list, handle both
        if isinstance(location, list):
            location_str = ' '.join(location).lower()
        else:
            location_str = location.lower()
        if any(loc in location_str for loc in preferred_locations):
            filtered.append(job)
    return filtered

def count_job_frequency(jobs):
    freq = {}
    for job in jobs:
        title = job.get('position', '').lower()
        freq[title] = freq.get(title, 0) + 1
    return freq

def rank_jobs(jobs, freq, resume_skills):
    ranked_jobs = []
    for job in jobs:
        title = job.get('position', '').lower()
        description = job.get('description', '') or job.get('tags', [])
        if isinstance(description, list):
            description_str = ' '.join(description).lower()
        else:
            description_str = description.lower()
        skill_match_score = sum(1 for skill in resume_skills if skill.lower() in description_str)
        frequency_score = freq.get(title, 0)
        total_score = skill_match_score * 2 + frequency_score  # weight skills higher
        ranked_jobs.append((total_score, job))
    ranked_jobs.sort(key=lambda x: x[0], reverse=True)
    return [job for _, job in ranked_jobs]

def fetch_remote_jobs(resume_skills):
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

    # Filter by preferred locations
    filtered = filter_jobs_by_location(filtered, PREFERRED_LOCATIONS)

    # Count frequency of job titles
    freq = count_job_frequency(filtered)

    # Rank jobs by frequency and skill match
    ranked = rank_jobs(filtered, freq, resume_skills)

    return ranked
