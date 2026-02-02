from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/jobs", tags=["Jobs"])


# -----------------------------
# Pydantic Schemas
# -----------------------------

class Job(BaseModel):
    id: int
    title: str
    company: str
    location: str
    tags: List[str]


class JobSearchRequest(BaseModel):
    query: str
    role: Optional[str] = None   # ✅ FIX (was required earlier)


# -----------------------------
# Mock Job Data (for now)
# -----------------------------

JOBS_DB = [
    {
        "id": 1,
        "title": "Frontend Developer Intern",
        "company": "TechCorp",
        "location": "Remote",
        "tags": ["React", "JavaScript", "HTML", "CSS"]
    },
    {
        "id": 2,
        "title": "Backend Developer Intern",
        "company": "InnovateX",
        "location": "Bangalore",
        "tags": ["Python", "FastAPI", "SQL"]
    },
    {
        "id": 3,
        "title": "Cloud Intern",
        "company": "Cloudify",
        "location": "Remote",
        "tags": ["AWS", "Docker", "Linux"]
    }
]


# -----------------------------
# Routes
# -----------------------------

@router.get("/available", response_model=List[Job])
def get_available_jobs():
    return JOBS_DB


@router.post("/search", response_model=List[Job])
def search_jobs(payload: JobSearchRequest):
    query = payload.query.lower()

    results = [
        job for job in JOBS_DB
        if query in job["title"].lower()
        or query in job["company"].lower()
        or any(query in tag.lower() for tag in job["tags"])
    ]

    return results
