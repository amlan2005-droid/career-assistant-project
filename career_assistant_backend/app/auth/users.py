from passlib.context import CryptContext
from app.models.user import User
from app.database.db import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db, username: str, password: str):
    hashed = pwd_context.hash(password)
    new_user = User(username=username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
