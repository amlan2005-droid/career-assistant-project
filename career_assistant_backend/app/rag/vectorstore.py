import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

DB_PATH = "app/rag/db_v2"


# -----------------------------
# Text Splitter
# -----------------------------
def get_text_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""],
    )


# -----------------------------
# Embeddings Factory
# -----------------------------
def get_embeddings():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if api_key:
        return GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=api_key
        )
    else:
        return OpenAIEmbeddings(
            model="text-embedding-3-small"
        )


# -----------------------------
# Load Vectorstore
# -----------------------------
def get_vectorstore():
    if not os.path.exists(DB_PATH):
        raise ValueError(
            f"Vectorstore not found at {DB_PATH}. "
            "Please run `python -m app.rag.ingest` first."
        )

    embeddings = get_embeddings()

    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )
