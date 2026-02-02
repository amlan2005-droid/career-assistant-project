from sqlalchemy import Column, Integer, ForeignKey
from app.database.db import Base

class JobMatchResult(Base):
    __tablename__ = "job_match_results"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    match_score = Column(Integer)  # 0–100
