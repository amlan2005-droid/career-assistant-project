from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.db import Base

class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    resume_text = Column(String)

    domains = Column(JSON)        # ["java-backend", "devops"]
    skills = Column(JSON)         # ["Spring Boot", "Docker"]
    experience_level = Column(String)
    resume_score = Column(Integer)

    strengths = Column(JSON)
    weaknesses = Column(JSON)
    suggestions = Column(JSON)
    achievement_density = Column(JSON)
    skill_insights = Column(JSON)  # [{"name": "Python", "confidence": 0.9, "level": "high"}]

    created_at = Column(DateTime(timezone=True), server_default=func.now())
