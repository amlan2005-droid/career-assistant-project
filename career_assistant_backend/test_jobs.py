from app.services.job_service import search_jobs_adzuna

if __name__ == "__main__":
    print("🔎 Testing Adzuna Job API...\n")

    # Example queries
    jobs = search_jobs_adzuna("cloud engineer", "Bangalore", 3)

    if jobs:
        print(f"✅ Found {len(jobs)} jobs\n")
        for i, job in enumerate(jobs, start=1):
            print(f"{i}. {job['title']} at {job['company']} ({job['location']})")
            print(f"   Salary: {job['salary']}")
            print(f"   Apply: {job['url']}\n")
    else:
        print("❌ No jobs returned. Check API key / parameters.")