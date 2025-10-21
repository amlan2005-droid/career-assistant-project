from app.database.db import Base, engine
from app.models.user import User
from app.models.resume import Resume
from app.models.job_match import JobMatchResult  # ✅ must be imported
from app.models.chat_history import ChatHistory

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print(" Done! career.db should now exist.")
