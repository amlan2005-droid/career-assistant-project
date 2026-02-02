from sqlalchemy import Column, Integer, JSON, ForeignKey
from app.database.db import Base

class ResumeProfile(Base):
    __tablename__ = "resume_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True)

    skills = Column(JSON)
    projects = Column(JSON)
    strengths = Column(JSON)
    weaknesses = Column(JSON)
