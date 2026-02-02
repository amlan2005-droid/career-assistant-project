import os
import re
from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

import google.api_core.exceptions
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai._common import GoogleGenerativeAIError
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

from app.rag.vectorstore import get_vectorstore
from app.rag.prompt import chat_prompt
from app.models.chat_history import ChatHistory


# Retry ONLY Gemini call
retry_on_llm_errors = retry(
    retry=retry_if_exception_type((
        google.api_core.exceptions.ResourceExhausted,
        google.api_core.exceptions.ServiceUnavailable,
        google.api_core.exceptions.DeadlineExceeded,
        google.api_core.exceptions.InternalServerError,
        GoogleGenerativeAIError,
    )),
    wait=wait_exponential(multiplier=2, min=5, max=60),
    stop=stop_after_attempt(5),
    reraise=True,
)


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        google_api_key=os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"),
        temperature=0.3,
        timeout=20,
        max_retries=0,  # prevent internal retries
    )


def save_message(db: Session, session_id: str, role: str, message: str):
    db.add(ChatHistory(
        session_id=session_id,
        role=role,
        message=message
    ))
    db.commit()


def get_recent_history(db: Session, session_id: str, limit: int = 6) -> str:
    messages = (
        db.query(ChatHistory)
        .filter(ChatHistory.session_id == session_id)
        .order_by(ChatHistory.timestamp.desc())  # Use timestamp, not created_at
        .limit(limit)
        .all()
    )

    messages.reverse()  # oldest → newest

    history = []
    for msg in messages:
        role = "User" if msg.role == "user" else "Assistant"
        history.append(f"{role}: {msg.message}")

    return "\n".join(history)


@retry_on_llm_errors
def run_rag_chain(message: str, history: str) -> str:
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {
            "context": itemgetter("question") | retriever | format_docs,
            "question": itemgetter("question"),
            "history": itemgetter("history"),
        }
        | chat_prompt
        | get_llm()
        | StrOutputParser()
    )

    return rag_chain.invoke({
        "question": message,
        "history": history,
    })


def handle_chat(db: Session, session_id: str, message: str) -> str:
    # Save user message ONCE
    save_message(db, session_id, "user", message)
    
    # Fetch history
    history = get_recent_history(db, session_id)

    try:
        response_text = run_rag_chain(message, history)
    except (google.api_core.exceptions.ResourceExhausted, GoogleGenerativeAIError, google.api_core.exceptions.NotFound) as e:
        error_msg = str(e).lower()
        if "resource_exhausted" in error_msg or "429" in error_msg:
            # Try to extract the wait time if it's there
            retry_match = re.search(r'retry in ([\d\.]+)s', error_msg)
            wait_time = f" {retry_match.group(0)}" if retry_match else ""
            response_text = (
                f"Gemini is taking a short breather! (Rate limit hit{wait_time}). "
                "The free-tier quota is a bit tight, but I've already tried retrying automatically. "
                "Please wait about 30 seconds before your next message so the quota can reset."
            )
        elif "not_found" in error_msg or "404" in error_msg:
            print(f"Chat model error (404): {e}")
            response_text = (
                "The configured AI model was not found or is unavailable for this API key. "
                "Please check your service configuration."
            )
        else:
            print(f"Chat error: {e}")
            response_text = "Sorry, I'm having trouble with the AI service right now."
    except Exception as e:
        import traceback
        traceback.print_exc()
        response_text = "Sorry, something went wrong while processing your request."

    save_message(db, session_id, "assistant", response_text)
    return response_text
