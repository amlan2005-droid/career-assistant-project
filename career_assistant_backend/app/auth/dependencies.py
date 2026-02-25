from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.auth.auth_bearer import AuthBearer, decode_jwt
from app.auth.users import get_user_by_username, get_user_by_id
from app.models.user import User

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(payload: dict = Depends(AuthBearer()), db: Session = Depends(get_db)) -> User:
    try:
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token does not contain user identification",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Ensure user_id is an integer
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = get_user_by_id(db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
