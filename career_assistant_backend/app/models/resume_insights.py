# models/resume_insights.py
from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.db import Base

class ResumeInsights(Base):
    __tablename__ = "resume_insights"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    domains = Column(String)  # comma-separated
    skills = Column(String)
