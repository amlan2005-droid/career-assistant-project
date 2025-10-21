def get_matched_jobs(user_skills, job_listings):
    matched_jobs = []
    for job in job_listings:
        required = job.get("skills", [])
        matched = set(user_skills).intersection(required)
        if matched:
            matched_jobs.append({
                "title": job["title"],
                "company": job["company"],
                "matched_skills": list(matched)
            })



