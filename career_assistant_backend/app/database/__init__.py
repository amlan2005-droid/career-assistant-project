from .db import SessionLocal, engine, Base

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
