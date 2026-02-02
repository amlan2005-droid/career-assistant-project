from pydantic import BaseModel
from typing import List


class InterviewQuestion(BaseModel):
    id: int
    question: str
    domain: str
    difficulty: str  # easy / medium / hard


class InterviewAnswer(BaseModel):
    question_id: int
    answer: str


class AnswerEvaluation(BaseModel):
    question_id: int
    score: float  # 0–10
    feedback: str
    mistakes: List[str]
    correct_points: List[str]


class InterviewResult(BaseModel):
    total_score: float        # 0–100
    technical_level: str      # Beginner / Intermediate / Advanced
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    answer_evaluations: List[AnswerEvaluation]
