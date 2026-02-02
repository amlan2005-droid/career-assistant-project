from pydantic import BaseModel
from typing import List

class ResumeAnalysisResponse(BaseModel):
    resume_id: int
    skills: List[str]
    experience_level: str
    resume_score: int
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    achievement_density: dict
