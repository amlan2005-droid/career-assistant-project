from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from uuid import uuid4
import uuid
import random
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.resume_analysis import ResumeAnalysis
from app.models.interview_session import InterviewSession
from app.services.resume_profile_service import get_resume_profile
from app.services.interview_engine import (
    generate_resume_aware_questions,
    generate_next_adaptive_question
)
from app.services.interview_evaluator import evaluate_answer, apply_cheating_penalty
from app.services.cheating_rules import CHEATING_SESSIONS

router = APIRouter(prefix="/interview", tags=["Interview"])

# In-memory sessions (backup/cache, but primary is DB)
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
def start_interview_endpoint(
    payload: StartInterviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume_profile = get_resume_profile(db, current_user.id)

    if not resume_profile:
        raise HTTPException(status_code=400, detail="Resume profile not found")

    if payload.question_count not in [5, 10, 15, 20]:
        raise HTTPException(status_code=400, detail="Question count must be 5, 10, 15, or 20")

    # Generate only the FIRST question initially for adaptive flow
    questions = generate_resume_aware_questions(
        domain=payload.domain,
        resume_profile=resume_profile,
        difficulty=payload.difficulty,
        question_count=1,
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
        total_questions=payload.question_count,
        questions=questions
    )

    db.add(session)
    db.commit()
    db.refresh(session)
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
def submit_answer_endpoint(
    payload: AnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(InterviewSession).filter(InterviewSession.id == payload.session_id).first()

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

    new_answers = list(session.answers) if session.answers else []
    new_scores = list(session.scores) if session.scores else []
    new_confid = list(session.confidences) if session.confidences else []

    new_answers.append(payload.answer)
    new_scores.append(evaluation["score"])
    new_confid.append(evaluation.get("confidence", 0.5))
    
    session.answers = new_answers
    session.scores = new_scores
    session.confidences = new_confid
    session.current_index += 1

    db.commit()
    db.refresh(session)

    if session.is_completed():
        difficulty_weight = {"easy": 0.8, "medium": 1.0, "hard": 1.2}
        summary = session.feedback_aggregator.generate_summary()
        
        # Apply Cheating Penalty
        cheating_session = CHEATING_SESSIONS.get(session.id, {"warnings": 0, "terminated": False})
        warnings_count = cheating_session.get("warnings", 0)
        is_terminated = cheating_session.get("terminated", False)
        
        raw_score = summary["average_score"] * 100 * difficulty_weight.get(session.difficulty, 1.0)
        final_score = apply_cheating_penalty(raw_score, warnings_count, is_terminated)
        final_score = min(100.0, final_score)
        
        # Save summary to DB
        session.feedback_summary = summary
        db.commit()
        db.refresh(session)

        # Basic report structure
        report = {"skills": []}
        for skill, scores in summary.get("skill_scores", {}).items():
            avg_skill_score = (sum(scores) / len(scores)) if scores else 0
            skill_score = min(100.0, avg_skill_score * 100 * difficulty_weight.get(session.difficulty, 1.0))
            
            report["skills"].append({
                "name": skill.capitalize(),
                "interview_score": f"{int(skill_score)}",
                "feedback": f"Average score for {skill}: {round(avg_skill_score, 2)}"
            })

        return {
            "interview_finished": True,
            "status": "answer recorded",
            "final_score_percentage": round(final_score, 2),
            "summary": summary,
            "report": report
        }

    # If the next question is already generated
    if len(session.questions) > session.current_index:
        return {
            "interview_finished": False,
            "status": "answer recorded",
            "question": session.questions[session.current_index],
            "question_number": session.current_index + 1
        }

    # Otherwise, generate the NEXT question adaptively
    state_summary = session.feedback_aggregator.generate_summary()
    
    next_q = generate_next_adaptive_question(
        domain=session.domain,
        difficulty=session.difficulty,
        state_summary=state_summary,
        previous_questions=session.questions
    )

    # Append new question to list
    existing_questions = list(session.questions) if session.questions else []
    existing_questions.append(next_q)
    session.questions = existing_questions
    
    db.commit()
    db.refresh(session)

    return {
        "interview_finished": False,
        "status": "answer recorded",
        "question": next_q,
        "question_number": session.current_index + 1
    }

# -----------------------------
# Get Next Question (Adaptive)
# -----------------------------
@router.get("/next/{session_id}")
def get_next_question(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    if session.is_completed():
        return {"interview_finished": True}

    # If the next question is already generated (e.g. from start or previous call)
    if len(session.questions) > session.current_index:
        return {
            "interview_finished": False,
            "question": session.questions[session.current_index],
            "question_number": session.current_index + 1
        }

    # Otherwise, generate the NEXT question adaptively
    state_summary = session.feedback_aggregator.generate_summary()
    
    next_q = generate_next_adaptive_question(
        domain=session.domain,
        difficulty=session.difficulty,
        state_summary=state_summary,
        previous_questions=session.questions
    )

    # Append new question to list
    existing_questions = list(session.questions) if session.questions else []
    existing_questions.append(next_q)
    session.questions = existing_questions
    
    db.commit()
    db.refresh(session)
    
    return {
        "interview_finished": False,
        "question": next_q,
        "question_number": session.current_index + 1
    }

# -----------------------------
# Interview State (Debug)
# -----------------------------
@router.get("/state/{session_id}")
def get_interview_state(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = sessions.get(session_id)
    if not session:
        session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized access to session state")
        
    return session.feedback_aggregator.generate_summary()

# -----------------------------
# Interview Summary
# -----------------------------
@router.get("/summary/{session_id}")
def interview_summary(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = sessions.get(session_id)
    
    if session:
        session = db.merge(session, load=False)
    else:
        session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
        if session:
            sessions[session_id] = session

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized access to session summary")

    if session.feedback_summary:
        return session.feedback_summary

    return session.feedback_aggregator.generate_summary()
