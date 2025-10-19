from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
print(">>> Running simple_backend.py from:", __file__)

# ----------------------
# CORS setup (allow React frontend)
# ----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# Expanded Job Data
# ----------------------
SAMPLE_JOBS = [
    {
        "id": 1,
        "title": "Cloud Engineer Intern",
        "company": "TechCloud",
        "location": "Bangalore",
        "tags": ["Azure", "Cloud Computing", "Python"],
        "salary": "₹20,000-30,000/month",
        "posted": "1 week ago",
        "description": "Learn cloud computing with Microsoft Azure platform.",
        "requirements": ["Python", "Basic Cloud Knowledge", "Linux", "Networking"],
        "type": "Internship",
        "experience": "Entry Level"
    },
    {
        "id": 2,
        "title": "Cloud Engineer",
        "company": "TechCorp",
        "location": "Bangalore",
        "tags": ["AWS", "Kubernetes", "DevOps"],
        "salary": "₹10-15 LPA",
        "posted": "2 weeks ago",
        "description": "Deploy and manage scalable cloud infrastructure on AWS.",
        "requirements": ["AWS", "Kubernetes", "Terraform"],
        "type": "Full-time",
        "experience": "2+ years"
    },
    # ... (rest of your jobs unchanged)
]

# ----------------------
# Utility
# ----------------------
def is_job_query(message: str) -> bool:
    if not message:
        return False
    keywords = ["job", "jobs", "hiring", "career", "internship", "role", "vacancy"]
    lower = message.lower()
    return any(k in lower for k in keywords)

# ----------------------
# Endpoints
# ----------------------
@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.get("/jobs/available")
async def available_jobs():
    # return jobs wrapped in an object for consistent parsing on frontend
    return {"jobs": SAMPLE_JOBS}

@app.get("/")
async def root():
    return {"message": "Career Assistant backend is running"}

@app.post("/jobs/search")
async def search_jobs(payload: dict):
    query = (payload.get("query") or "").strip().lower()
    if not query:
        return {"jobs": SAMPLE_JOBS}
    matches = [
        job for job in SAMPLE_JOBS
        if query in job.get("title", "").lower()
        or query in job.get("company", "").lower()
        or any(query in tag.lower() for tag in job.get("tags", []))
    ]
    return {"jobs": matches}

@app.post("/chatbot/session/new")
async def new_session():
    return {"session_id": "anon-session", "message": "session created"}

@app.post("/chatbot/message")
async def chatbot_message(payload: dict):
    user_message = (payload.get("message") or "").strip()
    if not user_message:
        return {"reply": "Please type something 🙂"}

    if is_job_query(user_message):
        jobs_list = "\n".join([f"{job['title']} at {job['company']}" for job in SAMPLE_JOBS])
        return {"reply": f"Here are some jobs you might like:\n{jobs_list}"}

    msg = user_message.lower()
    if "hello" in msg or "hi" in msg:
        return {"reply": "Hi there! 👋 How can I help you today?"}
    if "thank" in msg:
        return {"reply": "You're welcome! 😊"}
    if "bye" in msg:
        return {"reply": "Goodbye! Have a great day!"}

    return {"reply": "I'm sorry, I don't understand. Can you rephrase your question?"}
