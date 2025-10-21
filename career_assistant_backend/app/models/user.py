# app/models/user.py
from sqlalchemy import Column, Integer, String
from app.database.db import Base  # ✅ import Base from your db module

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
