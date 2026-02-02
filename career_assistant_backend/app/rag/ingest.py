import os
from dotenv import load_dotenv

load_dotenv()
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from app.rag.vectorstore import get_embeddings

DATA_PATH = "app/data"
DB_PATH = "app/rag/db_v2"

def load_documents():
    documents = []
    if not os.path.exists(DATA_PATH):
        print(f"⚠️ DATA_PATH {DATA_PATH} does not exist. Skipping document load.")
        return []

    for root, _, files in os.walk(DATA_PATH):
        for file in files:
            file_path = os.path.join(root, file)

            # Pick loader based on file type
            if file.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            elif file.endswith(".txt"):
                loader = TextLoader(file_path, encoding="utf-8")
            else:
                continue  # skip unsupported files

            # Load + add metadata
            docs = loader.load()
            for d in docs:
                d.metadata.update({
                    "source": root.split(os.sep)[-1],   # e.g. resumes / jobs / faqs
                    "filename": file                    # actual filename
                })
            documents.extend(docs)

    return documents

def ingest():
    print(" Loading documents...")
    documents = load_documents()

    if not documents:
        print("❌ No documents found to ingest.")
        return

    print(" Splitting into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    print(f" Loaded {len(documents)} documents, split into {len(docs)} chunks.")

    print(" Creating embeddings and storing in Chroma...")
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(docs, embeddings, persist_directory=DB_PATH)
    
    if hasattr(vectorstore, 'persist'):
        vectorstore.persist()

    print(f" Ingestion complete! Database saved at {DB_PATH}")

if __name__ == "__main__":
    ingest()
