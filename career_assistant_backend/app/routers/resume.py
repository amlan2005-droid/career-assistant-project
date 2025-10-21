import os
import shutil
import json
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.resume import Resume
from app.models.job_match import JobMatchResult
from app.services.resume_parser import parse_resume
from app.services.skill_extractor import extract_skills
from app.services.job_matcher import get_matched_jobs

router = APIRouter()
UPLOAD_DIR = "temp_resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Dependency to get DB session
def get_db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


@router.post("/analyze/")
async def analyze_resume(file: UploadFile = File(...), db: Session = Depends(get_db_session)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid file")

    # Temporary file path
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # Save the uploaded file
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Parse resume
        parsed = parse_resume(file_path)
        text = parsed.get("text", "")
        entities = parsed.get("entities", [])

        # Extract skills
        skill_pool = ["Python", "Django", "FastAPI", "SQL", "Java", "React", "Pandas", "Docker"]
        extracted_skills = extract_skills(text, skill_pool)

        # Example job listings (replace with DB later)
        job_listings = [
            {"title": "Software Engineer", "company": "Google", "skills": ["Python", "Django", "SQL"]},
            {"title": "Backend Developer", "company": "Startup", "skills": ["FastAPI", "PostgreSQL", "Docker"]},
            {"title": "Data Analyst", "company": "Analytics Inc", "skills": ["Python", "Pandas", "Excel"]},
        ]

        matched = get_matched_jobs(extracted_skills, job_listings)

        # Save resume in DB
        resume_record = Resume(text=text, entities=json.dumps(entities), user_id=None)
        db.add(resume_record)
        db.commit()
        db.refresh(resume_record)

        # Save matched jobs
        match_record = JobMatchResult(resume_id=resume_record.id, matched_jobs=json.dumps(matched))
        db.add(match_record)
        db.commit()

        # Return response
        return {
            "message": "Resume parsed and saved successfully",
            "resume_id": resume_record.id,
            "extracted_skills": extracted_skills,
            "matched_jobs": matched
        }

    finally:
        # Cleanup temp file
        if os.path.exists(file_path):
            os.remove(file_path)
