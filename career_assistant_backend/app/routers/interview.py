from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from uuid import uuid4
import random
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.resume_analysis import ResumeAnalysis
from app.models.interview_session import InterviewSession
from app.services.resume_profile_service import get_resume_profile
from app.services.interview_engine import generate_resume_aware_questions
from app.services.interview_evaluator import evaluate_answer

router = APIRouter(tags=["Interview"])

# In-memory sessions (temporary)
sessions = {}

# -----------------------------
# Request Models
# -----------------------------
class StartInterviewRequest(BaseModel):
    domain: str
    difficulty: str = "medium"
    question_count: int = 10

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

# -----------------------------
# Get Domains from Resume
# -----------------------------
@router.get("/domains")
def get_domains(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    analysis = (
        db.query(ResumeAnalysis)
        .filter(ResumeAnalysis.user_id == user.id)
        .order_by(ResumeAnalysis.created_at.desc())
        .first()
    )

    if not analysis or not analysis.domains:
        return {
            "domains": [],
            "message": "Upload resume to infer interview domains"
        }

    return {
        "domains": analysis.domains,
        "skill_insights": analysis.skill_insights or []
    }

# -----------------------------
# Start Interview
# -----------------------------
@router.post("/start")
def start_interview(
    payload: StartInterviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume_profile = get_resume_profile(db, current_user.id)

    if not resume_profile:
        raise HTTPException(status_code=400, detail="Resume profile not found")

    if payload.question_count not in [5, 10, 15, 20]:
        raise HTTPException(status_code=400, detail="Question count must be 5, 10, 15, or 20")

    questions = generate_resume_aware_questions(
        domain=payload.domain,
        resume_profile=resume_profile,
        difficulty=payload.difficulty,
        question_count=payload.question_count,
        previous_questions=[]
    )

    if not questions:
        raise HTTPException(status_code=400, detail="No questions generated")

    session_id = str(uuid4())

    session = InterviewSession(
        id=session_id,
        user_id=current_user.id,
        domain=payload.domain,
        difficulty=payload.difficulty,
        questions=questions
    )

    sessions[session_id] = session

    return {
        "session_id": session_id,
        "question": questions[0],
        "question_number": 1
    }

# -----------------------------
# Submit Answer
# -----------------------------
@router.post("/answer")
def submit_answer(
    payload: AnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = sessions.get(payload.session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized session access")

    current_question = session.questions[session.current_index]

    evaluation = evaluate_answer(
        question=current_question,
        answer=payload.answer,
        difficulty=session.difficulty
    )

    # Add feedback
    session.feedback_aggregator.add_feedback(
        skill=session.domain,
        evaluation=evaluation
    )

    session.answers.append(payload.answer)
    session.scores.append(evaluation["score"])
    session.current_index += 1

    if session.is_completed():
        difficulty_weight = {"easy": 0.8, "medium": 1.0, "hard": 1.2}
        base_avg = (sum(session.scores) / len(session.scores)) if session.scores else 0
        final_score = min(100.0, (base_avg / 10.0) * 100 * difficulty_weight.get(session.difficulty, 1.0))
        
        report = {"skills": []}
        summary = session.feedback_aggregator.generate_summary()
        
        for skill, data in summary.get("skills", {}).items():
            avg_skill_score = (sum(data["scores"]) / len(data["scores"])) if data["scores"] else 0
            skill_score = min(100.0, (avg_skill_score / 10.0) * 100 * difficulty_weight.get(session.difficulty, 1.0))
            
            resume_confidence = "75"
            analysis = db.query(ResumeAnalysis).filter(ResumeAnalysis.user_id == current_user.id).order_by(ResumeAnalysis.created_at.desc()).first()
            
            if analysis and analysis.skill_insights:
                for insight in analysis.skill_insights:
                    if insight.get("name", "").lower() in skill.lower():
                        resume_confidence = f"{int(insight.get('confidence', 0.8) * 100)}"
                        break

            report["skills"].append({
                "name": skill.capitalize(),
                "resume_confidence": resume_confidence,
                "interview_score": f"{int(skill_score)}",
                "feedback": f"Strong in {', '.join(data['strengths'][:2]) if data['strengths'] else 'basics'}. " + 
                           f"Needs focus on {', '.join(data['weaknesses'][:2]) if data['weaknesses'] else 'advanced topics'}."
            })

        if not report["skills"]:
            report["skills"] = [{
                "name": session.domain.capitalize(),
                "resume_confidence": "70",
                "interview_score": f"{int(final_score)}",
                "feedback": "Overall performance analysis."
            }]

        return {
            "interview_finished": True,
            "final_score_percentage": round(final_score, 2),
            "message": "Interview completed successfully",
            "report": report
        }

    return {
        "interview_finished": False,
        "question_number": session.current_index + 1,
        "question": session.questions[session.current_index],
        "feedback": evaluation
    }

# -----------------------------
# Interview Summary
# -----------------------------
@router.get("/summary/{session_id}")
def interview_summary(session_id: str):
    session = sessions.get(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session.feedback_aggregator.generate_summary()
