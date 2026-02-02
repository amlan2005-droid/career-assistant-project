import os
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.db import get_db
from app.models.chat_history import ChatHistory
from app.services.chat_services import handle_chat
from app.utils.limiter import limiter

# --------------------------------------------------
# Router
# --------------------------------------------------
router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

# --------------------------------------------------
# Models
# --------------------------------------------------
class ChatQuery(BaseModel):
    query: str

# --------------------------------------------------
# Create new chat session
# --------------------------------------------------
@router.post("/session/new")
def create_session(db: Session = Depends(get_db)):
    session = ChatHistory.create_session(db)
    return {"session_id": session}

# --------------------------------------------------
# Main Chat Endpoint (RAG + Gemini)
# --------------------------------------------------
@router.post("/session/{session_id}/query")
@limiter.limit("1/8seconds")  # ⏱ 1 message per 8 seconds
def chat_query(
    request: Request,
    session_id: str,
    payload: ChatQuery,
    db: Session = Depends(get_db)
):
    query = payload.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Empty message")

    answer = handle_chat(db, session_id, query)
    return {"reply": answer}
