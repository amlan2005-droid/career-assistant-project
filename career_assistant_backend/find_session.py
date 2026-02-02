from sqlalchemy import create_engine, select, desc
from sqlalchemy.orm import sessionmaker
from app.database.db import Base
from app.models.chat_history import ChatHistory

DATABASE_URL = "sqlite:///./career.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Query the last 5 unique sessions with their most recent message
from sqlalchemy import func

subquery = (
    db.query(
        ChatHistory.session_id,
        func.max(ChatHistory.timestamp).label("max_ts")
    )
    .group_by(ChatHistory.session_id)
    .subquery()
)

recent_sessions = (
    db.query(ChatHistory.session_id, ChatHistory.timestamp, ChatHistory.message)
    .join(subquery, (ChatHistory.session_id == subquery.c.session_id) & (ChatHistory.timestamp == subquery.c.max_ts))
    .order_by(desc(ChatHistory.timestamp))
    .limit(5)
    .all()
)

if recent_sessions:
    with open("session_results.txt", "w") as f:
        f.write("RECENT_SESSIONS_START\n")
        for sess in recent_sessions:
            f.write(f"ID: {sess[0]} | TIME: {sess[1]} | MSG: {sess[2][:50]}...\n")
        f.write("RECENT_SESSIONS_END\n")
    print("RESULTS_SAVED_TO_FILE")
else:
    print("NO_SESSION_FOUND")
db.close()
