from fastapi import FastAPI
from dotenv import load_dotenv
from app.routers import auth, resume, job_match, interview, query as query_router, chat, job
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env at startup
load_dotenv()

app = FastAPI(title="Career Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(resume.router, prefix="/resume")
app.include_router(job_match.router, prefix="/jobs",tags=["Job"])
app.include_router(interview.router, prefix="/interview")
app.include_router(query_router.router, prefix="/query", tags=["Query"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(job.router, prefix="/job", tags=["job"])

@app.get("/")
def root():
    return {"message": "Career Assistant Backend is live!"}

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "pong"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Career Assistant API is running",
        "version": "1.0.0"
    }

@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint is working!"}

