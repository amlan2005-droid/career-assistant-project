import sys
import traceback

# Add project root to sys.path
sys.path.append('.')

try:
    from app.models.interview_session import InterviewSession
    from app.database.db import Base
    
    # Test instantiation
    print("Testing InterviewSession instantiation...")
    session = InterviewSession(
        id="test-id",
        user_id=1,
        domain="python",
        difficulty="medium",
        questions=["q1", "q2"]
    )
    print("Instantiation Success!")
    print(f"Answers: {session.answers}")
    print(f"Scores: {session.scores}")
    print(f"Index: {session.current_index}")
    
except Exception:
    print("DIAGNOSTIC FAILED:")
    traceback.print_exc()
