import json

data = {
    "matched_jobs": [
        {"title": "Software Engineer", "company": "Google", "matched_skills": ["SQL", "Python"]},
        {"title": "Backend Developer", "company": "Startup", "matched_skills": ["Docker"]},
        {"title": "Data Analyst", "company": "Analytics Inc", "matched_skills": ["Python"]}
    ]
}

with open("matched_jobs.json", "w") as f:
    json.dump(data, f, indent=4)

print("✅ Saved to matched_jobs.json")
