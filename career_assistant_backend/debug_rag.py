import os
import sys
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma

# Path to the persistent ChromaDB
DB_PATH = "app/rag/db"

def check_api_key():
    print(" Checking API Key...")
    if os.getenv("GOOGLE_API_KEY"):
        print(" Using Google Gemini API Key.")
        try:
            llm = ChatGoogleGenerativeAI(model="models/gemini-flash-latest", temperature=0)
            llm.invoke("Hello")
            print(" API Key is valid (LLM response received).")
            return True
        except Exception as e:
            print(f" API Key check failed: {e}")
            return False
    else:
        print(" Checking OpenAI API Key...")
        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            print("OPENAI_API_KEY is missing from environment variables.")
            return False
        
        try:
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            llm.invoke("Hello")
            print(" API Key is valid (LLM response received).")
            return True
        except Exception as e:
            print(f" API Key check failed: {e}")
            return False

def check_vectorstore():
    print(f"\n Checking Vector Store at {DB_PATH}...")
    if not os.path.exists(DB_PATH):
        print(f" Vector store directory does not exist at {DB_PATH}.")
        return

    try:
        if os.getenv("GOOGLE_API_KEY"):
            embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        else:
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
        count = vectorstore._collection.count()
        print(f" Vector store loaded. Document count: {count}")
        
        if count == 0:
            print(" Vector store is empty! RAG will not work.")
    except Exception as e:
        print(f" Failed to load vector store: {e}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    if check_api_key():
        check_vectorstore()
