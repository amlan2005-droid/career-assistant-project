import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

VECTORSTORE_PATH = "vectorstore_index"

def build_vectorstore_from_text(text: str):
    # 1. Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_text(text)

    # 2. Create embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # 3. Build vectorstore
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)

    # 4. Save locally
    vectorstore.save_local(VECTORSTORE_PATH)

    return vectorstore

def get_vectorstore():
    """Load vectorstore if it exists, otherwise build a new one."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    if os.path.exists(VECTORSTORE_PATH):
        return FAISS.load_local(VECTORSTORE_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        raise ValueError("Vectorstore not found. Please build it first.")
