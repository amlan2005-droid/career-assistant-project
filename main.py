from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from app.routers import resume, job_match, interview
from app.routers import auth_routes
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="Career Assistant API")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryInput(BaseModel):
    question: str

# Include routers (only include each router once)
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(resume.router, prefix="/resume", tags=["Resume"])
app.include_router(job_match.router, prefix="/jobs", tags=["Job"])
app.include_router(interview.router, prefix="/interview", tags=["Interview"])

@app.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    # Mock analysis logic
    base_score = random.randint(65, 85)
    adi_score = round(random.uniform(3.0, 7.5), 1)
    
    analysis = {
        "resume_score": base_score,
        "experience_level": "Intermediate" if base_score > 75 else "Entry Level",
        "skills": ["Python", "FastAPI", "React", "Tailwind CSS", "JavaScript", "SQL"],
        "strengths": [
            "Strong technical stack alignment",
            "Quantifiable achievements detected",
            "Professional formatting and structure"
        ],
        "weaknesses": [],
        "suggestions": [
            "Add more specific metrics for your latest role",
            "Consider adding a summary section at the top",
            "Include links to relevant portfolio projects"
        ],
        "achievement_density_index": {
            "adi_score": adi_score,
            "metrics_found": random.randint(3, 8)
        }
    }
    
    return {"analysis": analysis}

@app.get("/")
def root():
    return {"message": "Career Assistant Backend is live!"}

@app.post("/query")
async def query(input: QueryInput):
    # Replace with your AI logic or OpenAI integration
    return {"answer": f"You asked: {input.question}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


