from fastapi import APIRouter, Body
from app.services.cheating_rules import CheatingRulesEngine, process_cheating_event
from app.services.cv_engine import CVEngine, CVStatus

router = APIRouter()

# TEMP in-memory store (later: Redis/DB)
SESSION_RULES = {}
SESSION_CV_ENGINES = {}

def get_engine(session_id: str):
    if session_id not in SESSION_RULES:
        SESSION_RULES[session_id] = CheatingRulesEngine()
    return SESSION_RULES[session_id]

def get_cv_engine(session_id: str):
    if session_id not in SESSION_CV_ENGINES:
        SESSION_CV_ENGINES[session_id] = CVEngine()
    return SESSION_CV_ENGINES[session_id]

@router.get("/cheating/status/{session_id}")
def cheating_status(session_id: str):
    engine = get_engine(session_id)
    return engine.summary()

@router.post("/cheating/event")
def cheating_event(payload: dict):
    session_id = payload["session_id"]
    event_type = payload["event_type"]

    result = process_cheating_event(session_id, event_type)
    return result

@router.post("/cheating/tab-switch")
def tab_switch(session_id: str = Body(..., embed=True)):
    engine = get_engine(session_id)
    engine.tab_switch_detected()
    return {"status": "ok"}

@router.post("/cheating/frame")
def analyze_frame(session_id: str = Body(...), frame: str = Body(...)):
    engine = get_engine(session_id)
    cv_engine = get_cv_engine(session_id)
    
    result = cv_engine.analyze_frame(frame)
    status = result["status"]
    
    if status == CVStatus.NO_FACE.value:
        process_cheating_event(session_id, "face_missing")
    elif status == CVStatus.MULTIPLE_FACES.value:
        process_cheating_event(session_id, "multiple_faces")
    elif status == CVStatus.EYES_NOT_DETECTED.value:
        process_cheating_event(session_id, "gaze_off_screen")
        
    return result
