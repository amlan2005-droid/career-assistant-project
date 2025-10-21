from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.db import Base

class JobMatchResult(Base):
    __tablename__ = "job_match_results"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    matched_jobs = Column(String)
