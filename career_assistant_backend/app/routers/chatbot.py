from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.chat_services import handle_chat

router = APIRouter(prefix="/chat", tags=["Chatbot"])

@router.post("/{session_id}")
def chat(session_id: str, message: str, db: Session = Depends(get_db)):
    response = handle_chat(db, session_id, message)
    return {"session_id": session_id, "response": response}
