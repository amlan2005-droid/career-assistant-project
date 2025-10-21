from sqlalchemy.orm import Session
from app.models.chat_history import ChatHistory

__all__ = [
    "save_message",
    "get_messages",
    "clear_messages",
    "handle_chat",
]


def save_message(db: Session, session_id: str, role: str, message: str) -> ChatHistory:
    chat = ChatHistory(session_id=session_id, role=role, message=message)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def get_messages(db: Session, session_id: str) -> list[ChatHistory]:
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.session_id == session_id)
        .order_by(ChatHistory.timestamp.asc())
        .all()
    )


def clear_messages(db: Session, session_id: str) -> int:
    deleted = (
        db.query(ChatHistory)
        .filter(ChatHistory.session_id == session_id)
        .delete(synchronize_session=False)
    )
    db.commit()
    return deleted


def handle_chat(db: Session, session_id: str, message: str) -> str:
    """Simple chat handler that echoes back the user's message.

    Persists both the user message and the assistant response to chat history.
    """
    # Save the incoming user message
    save_message(db, session_id=session_id, role="user", message=message)

    # Generate a basic response (placeholder for real LLM integration)
    response_text: str = f"You said: {message}"

    # Save the assistant's response
    save_message(db, session_id=session_id, role="assistant", message=response_text)

    return response_text
