
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

def test_embeddings(model_name):
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    print(f"Testing embedding model: {model_name}")
    
    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model=model_name,
            google_api_key=api_key
        )
        vector = embeddings.embed_query("test query")
        print(f"✅ Success for {model_name}: Vector length {len(vector)}")
        return True
    except Exception as e:
        print(f"❌ Failed for {model_name}: {e}")
        return False

if __name__ == "__main__":
    # Test current one
    test_embeddings("models/embedding-001")
    # Test suspected correct one
    test_embeddings("models/gemini-embedding-001")
    # Test without prefix
    test_embeddings("text-embedding-004")
