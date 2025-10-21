from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.job_service import search_jobs_adzuna

router = APIRouter()

class JobSearchRequest(BaseModel):
    role: str
    location: str = "India"
    results_per_page: int = 5

@router.post("/jobs/search")
async def search_jobs(request: JobSearchRequest):
    try:
        jobs = search_jobs_adzuna(
            role=request.role,
            location=request.location,
            results_per_page=request.results_per_page
        )
        return {"results": jobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
