from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import random
import uuid

app = FastAPI(title="Career Assistant Backend")

# ----------------------
# CORS
# ----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# State
# ----------------------
sessions = {}

# ----------------------
# Sample Job Data
# ----------------------
SAMPLE_JOBS = [
    {
        "id": 1,
        "title": "Cloud Engineer Intern",
        "company": "TechCloud",
        "location": "Bangalore",
        "tags": ["Azure", "Cloud Computing", "Python"],
    },
    {
        "id": 2,
        "title": "Cloud Engineer",
        "company": "TechCorp",
        "location": "Bangalore",
        "tags": ["AWS", "Kubernetes", "DevOps"],
    },
]

# ----------------------
# Utils
# ----------------------
def is_job_query(message: str) -> bool:
    keywords = ["job", "jobs", "hiring", "career", "internship", "role"]
    return any(k in message.lower() for k in keywords)

# ----------------------
# Health
# ----------------------
@app.get("/ping")
async def ping():
    return {"message": "pong"}

# ----------------------
# Jobs
# ----------------------
@app.get("/jobs/available")
async def available_jobs():
    return {"jobs": SAMPLE_JOBS}

@app.post("/jobs/search")
async def search_jobs(payload: dict):
    query = payload.get("query", "").lower()
    if not query:
        return {"jobs": SAMPLE_JOBS}

    matches = [
        job for job in SAMPLE_JOBS
        if query in job["title"].lower()
        or query in job["company"].lower()
        or any(query in tag.lower() for tag in job["tags"])
    ]
    return {"jobs": matches}

# ----------------------
# Resume Analysis
# ----------------------
@app.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    # Mock analysis logic for lightweight backend
    # In a real app, you would parse the PDF/DOCX here
    
    filename = file.filename.lower()
    
    # Randomize some scores for variety
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

# ----------------------
# Chatbot
# ----------------------
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "anon-session"

class InterviewStartRequest(BaseModel):
    domain: str

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

@app.post("/chatbot/session/new")
async def new_session():
    return {"session_id": "anon-session", "message": "session created"}

@app.post("/chatbot/message")
async def chatbot_message(req: ChatRequest):
    msg = req.message.strip()

    if not msg:
        return {"reply": "Please type something "}

    if is_job_query(msg):
        jobs = "\n".join(
            f"{job['title']} at {job['company']}" for job in SAMPLE_JOBS
        )
        return {"reply": f"Here are some jobs you might like:\n{jobs}"}

    msg_lower = msg.lower()
    if "hello" in msg_lower or "hi" in msg_lower:
        return {"reply": "Hi there! How can I help you today?"}
    if "thank" in msg_lower:
        return {"reply": "You're welcome! "}
    if "bye" in msg_lower:
        return {"reply": "Goodbye! Have a great day!"}

    return {"reply": "I'm not sure I understood. Can you rephrase?"}

# ----------------------
# Interview
# ----------------------
# Sample interview questions by domain
INTERVIEW_QUESTIONS = {
    "python": [
        "What is the difference between a list and a tuple in Python?",
        "Explain the concept of decorators in Python.",
        "What is a generator and how does it differ from a regular function?",
        "How does Python's garbage collection work?",
        "What are Python's magic methods? Give some examples."
    ],
    "backend": [
        "What is the difference between REST and GraphQL?",
        "Explain the concept of database indexing.",
        "What are microservices and what are their advantages?",
        "How would you handle authentication in a web application?",
        "What is the CAP theorem?"
    ],
    "hr": [
        "Tell me about yourself.",
        "What are your greatest strengths?",
        "Where do you see yourself in 5 years?",
        "Describe a challenging situation you faced and how you handled it.",
        "Why do you want to work for our company?"
    ],
    "frontend": [
        "What is the virtual DOM and how does it work?",
        "Explain the difference between var, let, and const in JavaScript.",
        "What are React hooks and why are they useful?",
        "How would you optimize the performance of a web application?",
        "What is the difference between CSS Grid and Flexbox?"
    ],
    "data-science": [
        "What is the difference between supervised and unsupervised learning?",
        "Explain the bias-variance tradeoff.",
        "What is overfitting and how can you prevent it?",
        "Describe the difference between classification and regression.",
        "What is cross-validation and why is it important?"
    ]
}

@app.get("/interview/domains")
async def get_interview_domains():
    """
    Returns available interview domains.
    In a real app, this could be filtered based on the user's resume skills.
    """
    domains = list(INTERVIEW_QUESTIONS.keys())
    return {"domains": domains}

@app.post("/interview/start")
async def start_interview(req: InterviewStartRequest):
    """
    Starts a new interview session for the given domain.
    Returns session_id, first question, and question_number.
    """
    domain = req.domain.lower()
    
    # Validate domain
    if domain not in INTERVIEW_QUESTIONS:
        return {
            "error": f"Invalid domain. Available domains: {list(INTERVIEW_QUESTIONS.keys())}"
        }
    
    # Generate unique session ID
    session_id = str(uuid.uuid4())
    
    # Get first question
    questions = INTERVIEW_QUESTIONS[domain]
    first_question = questions[0] if questions else "No questions available for this domain."

    # Store session
    sessions[session_id] = {
        "domain": domain,
        "questions": questions,
        "current": 0,
        "scores": []
    }
    
    return {
        "session_id": session_id,
        "question": first_question,
        "question_number": 1,
        "total_questions": len(questions)
    }

@app.post("/interview/answer")
async def submit_answer(payload: AnswerRequest):
    session = sessions.get(payload.session_id)
    if not session:
        return {"error": "Session not found"}
        
    # Mock score
    score = random.randint(5, 9)
    session["scores"].append(score)
    session["current"] += 1
    
    if session["current"] >= len(session["questions"]):
        final_score = sum(session["scores"]) / len(session["scores"]) * 10
        
        # Mock Report
        report = {
            "skills": [
                {
                    "name": session["domain"].capitalize(),
                    "resume_confidence": "85",
                    "interview_score": str(int(final_score)),
                    "feedback": "Great performance in the technical session."
                },
                {
                    "name": "Communication",
                    "resume_confidence": "80",
                    "interview_score": str(int(final_score + 5)),
                    "feedback": "Clear and concise explanation of concepts."
                }
            ]
        }
        
        return {
            "interview_finished": True,
            "final_score_percentage": round(final_score, 2),
            "message": "Interview completed successfully",
            "report": report
        }
        
    next_q = session["questions"][session["current"]]
    return {
        "interview_finished": False,
        "question_number": session["current"] + 1,
        "question": next_q
    }
