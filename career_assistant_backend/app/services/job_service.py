import requests

# ✅ Your Adzuna credentials
ADZUNA_APP_ID = "9de4b82d"
ADZUNA_APP_KEY = "731f10318302f79cc2b5c6d56fa62c1c"

# ✅ Base URL for India jobs (you can switch "in" → "us" / "gb" / etc.)
ADZUNA_API_URL = "https://api.adzuna.com/v1/api/jobs/in/search/1"


def search_jobs_adzuna(role: str, location: str = "India", results_per_page: int = 5):
    """
    Fetch jobs from Adzuna API for a given role and location.
    """

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": role,
        "where": location,
        "results_per_page": results_per_page,
        "content-type": "application/json"
    }

    try:
        print(f"🌍 Calling Adzuna API with params: {params}")
        r = requests.get(ADZUNA_API_URL, params=params, timeout=8)

        # Check for errors
        r.raise_for_status()

        data = r.json()

        jobs = []
        for j in data.get("results", []):
            jobs.append({
                "title": j.get("title"),
                "company": j.get("company", {}).get("display_name", "Unknown"),
                "location": j.get("location", {}).get("display_name", "Unknown"),
                "salary": f"{j.get('salary_min', 'N/A')} - {j.get('salary_max', 'N/A')}" 
                          if j.get("salary_min") else "N/A",
                "url": j.get("redirect_url", "#")
            })

        print(f"✅ Parsed {len(jobs)} jobs")
        return jobs

    except requests.exceptions.RequestException as e:
        print("❌ Request error:", str(e))
        return []

    except Exception as e:
        print("❌ Unexpected error:", str(e))
        return []
