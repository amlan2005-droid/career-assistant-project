from fastapi import APIRouter, Depends, HTTPException
import json
from typing import Tuple, List, Dict, Any
from pydantic import BaseModel
from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryMemory

from app.database import get_db
from app.rag.vectorstore import get_vectorstore
from app.services.chat_services import save_message, get_messages, clear_messages
from app.services.job_service import search_jobs_adzuna

router = APIRouter()

# Request models
class QueryRequest(BaseModel):
    question: str
    session_id: str  # ✅ independent user sessions


# Custom prompt
template = """
You are a helpful career assistant. Use the provided context and conversation history
to answer the current question.

If the answer comes from a document, include the source and filename in parentheses at the end.
Example: (Source: resumes / john_doe.pdf)

Context:
{context}

Conversation history (summarized if long):
{chat_history}

Question: {question}
Answer:
"""
QA_PROMPT = PromptTemplate(
    template=template,
    input_variables=["context", "question", "chat_history"]
)  


def is_job_query(question: str) -> bool:
    """Check if the question is asking for job-related information."""
    job_keywords = [
 "job", "jobs", "career", "position", "opening", "vacancy",
        "employment", "hiring", "recruit", "work", "role"
    ]
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in job_keywords)


def get_chain(db: Session, session_id: str):
    """Conversational chain with hybrid memory (DB + summarization)."""
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Summary memory for long chats
    summary_memory = ConversationSummaryMemory(
        llm=llm,
        memory_key="chat_history",
        return_messages=True
    )

    # Preload past history from DB
    history = get_messages(db, session_id)
    for m in history:
        message: str = str(m.message)
        if str(m.role) == "user":
            summary_memory.chat_memory.add_user_message(message)
        else:
            summary_memory.chat_memory.add_ai_message(message)

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=summary_memory,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT}
    )


def _parse_job_query(question: str) -> Tuple[str, str]:
    """Extracts role and location from a job-related question."""
    question_lower = question.lower()
    # A simple parser: assumes "jobs for [role] in [location]" or just "[role] jobs"
    parts = question_lower.split(" in ")
    role_part = parts[0]
    location = parts[1].strip() if len(parts) > 1 else "India"

    # Clean up role text
    role = role_part.replace("show me jobs for", "").replace("jobs for", "").replace("jobs", "").strip()
    
    # Default if parsing fails to find a role
    if not role:
        role = "engineer"
        
    print(f"🔎 Extracted role: '{role}', location: '{location}'")
    return role, location


def _format_job_results(jobs: List[Dict[str, Any]], source: str) -> str:
    """Formats a list of job dictionaries into a readable string."""
    if source == "api":
        return "\n\n".join(
            [f"**{job.get('title', 'N/A')}** at {job.get('company', {}).get('display_name', 'N/A')} "
             f"({job.get('location', {}).get('display_name', 'N/A')})\n"
             f"Salary: {job.get('salary_min', 'N/A')} - {job.get('salary_max', 'N/A')}\n"
             f"[Apply Here]({job.get('redirect_url', '#')})"
             for job in jobs]
        )
    # Fallback for local JSON structure
    return "\n\n".join(
        [f"**{job.get('title', 'Unknown')}** at {job.get('company', 'Unknown')}\n"
         f"Matched Skills: {', '.join(job.get('matched_skills', []))}"
         for job in jobs]
    )


def _handle_offline_job_search(role: str) -> str:
    """Handles job search using the local JSON file as a fallback."""
    print("⚠️ API failed or returned no results, using offline data.")
    try:
        with open("app/routers/matched_jobs.json", "r") as f:
            offline_jobs = json.load(f)["matched_jobs"]
        
        # Filter offline jobs by role (simple substring match)
        if role and role.lower() != 'any':
            offline_jobs = [
                j for j in offline_jobs 
                if role.lower() in j.get("title", "").lower()
            ]

        if not offline_jobs:
            return f"We couldn't find any jobs for *{role}* right now, and our offline cache is empty or doesn't have a match."

        formatted_jobs = _format_job_results(offline_jobs, source="local")
        return f"We're having trouble reaching our job provider, but here are some popular jobs for *{role}* from our local cache:\n\n{formatted_jobs}"

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"🚨 Error reading offline jobs cache: {e}")
        return f"We couldn't find any jobs for *{role}* right now, and our offline cache is currently unavailable."


async def _handle_job_query(question: str) -> str:
    """Orchestrates the job search logic."""
    print("✅ Detected job-related query")
    role, location = _parse_job_query(question)

    # Fetch jobs from Adzuna
    jobs = search_jobs_adzuna(role, location, results_per_page=3)
    print(f"📊 Adzuna API returned {len(jobs)} jobs")

    if not jobs:
        return _handle_offline_job_search(role)
    
    formatted_jobs = _format_job_results(jobs, source="api")
    return f"Here are some job openings for *{role}* in *{location}*:\n\n{formatted_jobs}"


async def _handle_rag_query(question: str, session_id: str, db: Session) -> Dict[str, Any]:
    """Handles a general query using the RAG chain."""
    print("🟡 Query is NOT job related → sending to RAG")
    chain = get_chain(db, session_id)
    result = chain.invoke({"question": question})
    
    sources = []
    if "source_documents" in result:
        for doc in result["source_documents"]:
            src = doc.metadata.get("source", "unknown")
            fname = doc.metadata.get("filename", "unknown")
            sources.append(f"{src} / {fname}")

    return {"answer": result["answer"], "sources": list(set(sources))}


@router.post("/query")
async def query(request: QueryRequest, db: Session = Depends(get_db)):
    try:
        print(f"\n🟢 Incoming question: {request.question}")
        save_message(db, request.session_id, "user", request.question)

        if is_job_query(request.question):
            answer = await _handle_job_query(request.question)
            response_data = {"answer": answer, "sources": []}
        else:
            response_data = await _handle_rag_query(request.question, request.session_id, db)
        
        save_message(db, request.session_id, "assistant", response_data["answer"])
        return response_data

    except Exception as e:
        print(f"❌ ERROR in /query endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.delete("/reset/{session_id}")
async def reset(session_id: str, db: Session = Depends(get_db)):
    try:
        clear_messages(db, session_id)
        return {"message": f"Chat history for session {session_id} has been cleared."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))