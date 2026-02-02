from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.job_service import search_jobs_adzuna

router = APIRouter()

class JobSearchRequest(BaseModel):
    role: str
    location: str = "India"
    results_per_page: int = 5

@router.post("/search")
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

@router.get("/available")
async def get_available_jobs():
    """Get available jobs - returns sample jobs or searches for general positions"""
    try:
        # Search for general tech jobs as a default
        jobs = search_jobs_adzuna(
            role="software engineer",
            location="India",
            results_per_page=10
        )
        return {"results": jobs, "count": len(jobs)}
    except Exception as e:
        # Return empty list if API fails
        return {"results": [], "count": 0, "error": str(e)}
