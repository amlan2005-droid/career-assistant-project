import requests

BASE_URL = "http://127.0.0.1:8000"

def test_query():
    # 1. Create a session
    resp = requests.post(f"{BASE_URL}/chatbot/session/new")
    if resp.status_code != 200:
        print(f"Failed to create session: {resp.status_code} {resp.text}")
        return
    
    session_id = resp.json().get("session_id")
    print(f"Created session: {session_id}")

    # 2. Test query
    payload = {"query": "Hello, how can you help me?"}
    query_url = f"{BASE_URL}/chatbot/session/{session_id}/query"
    print(f"Testing POST {query_url} with payload {payload}")
    
    resp = requests.post(query_url, json=payload)
    print(f"Response Status: {resp.status_code}")
    try:
        print(f"Response Body: {resp.json()}")
    except:
        print(f"Response Body (text): {resp.text}")

if __name__ == "__main__":
    test_query()
