import sys
sys.path.append('.')

try:
    from app.models.interview_session import InterviewSession
    print(f"Table Name: {InterviewSession.__tablename__}")
    print(f"Columns: {InterviewSession.__table__.columns.keys()}")
    
    print("Attempting to instantiate InterviewSession(id='test')...")
    s = InterviewSession(id='test')
    print("Success!")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
