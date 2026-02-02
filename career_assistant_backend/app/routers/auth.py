from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import cast

from app.database.db import get_db
from app.models.user import User
from app.schemas.auth_schemas import UserCreate, UserLogin, TokenResponse
from app.auth.auth_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔒 Password utility functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 🧍‍♂️ Register user
@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_pw = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token({"sub": str(new_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


# 🔐 Login user
@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    # ✅ Use cast() here to remove Pylance warning
    if not db_user or not verify_password(user.password, cast(str, db_user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
