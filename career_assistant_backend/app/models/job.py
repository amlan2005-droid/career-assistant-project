from sqlalchemy import Column, Integer, String, Text
from app.database.db import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String)
    skills = Column(String)        # Python, SQL, AWS
    experience = Column(String)    # Fresher / 0–2 yrs
    description = Column(Text)
    apply_link = Column(String)
