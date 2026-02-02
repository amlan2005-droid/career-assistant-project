# app/models/resume.py
from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.db import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    entities = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
