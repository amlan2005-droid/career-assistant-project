from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
import json

from app.database.db import SessionLocal
from app.models.job_match import JobMatchResult

router = APIRouter()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/resume/{resume_id}/matches")
def get_job_matches(
    resume_id: int = Path(..., description="ID of the resume"),
    db: Session = Depends(get_db)
):
    match = db.query(JobMatchResult).filter(JobMatchResult.resume_id == resume_id).first()

    if not match:
        raise HTTPException(status_code=404, detail="No job matches found for this resume")

    try:
        matched_jobs = json.loads(match.matched_jobs) if isinstance(match.matched_jobs, str) else match.matched_jobs
    except json.JSONDecodeError:
        matched_jobs = []  # fallback if corrupted

    return {
        "resume_id": resume_id,
        "matched_jobs": matched_jobs
    }
