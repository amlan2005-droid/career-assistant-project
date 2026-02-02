from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    auth,
    resume,
    job_match,
    interview,
    chatbot,
)
from app.routers.jobs import router as jobs_router

from app.database.db import Base, engine
from app.models.user import User
from app.models.resume import Resume
from app.models.job_match import JobMatchResult
from app.models.chat_history import ChatHistory
from app.models.resume_analysis import ResumeAnalysis
from app.models.resume_insights import ResumeInsights

from app.utils.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI(
    title="Career Assistant API",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "Career Assistant API running"}

@app.get("/ping")
async def ping():
    return {"status": "ok"}

#  ROUTERS
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(job_match.router, prefix="/jobs", tags=["Job Matching"])
app.include_router(interview.router, prefix="/interview", tags=["Interview"])
app.include_router(chatbot.router)
app.include_router(jobs_router)

Base.metadata.create_all(bind=engine)
