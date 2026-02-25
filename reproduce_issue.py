import requests

<<<<<<< HEAD
url = "http://127.0.0.1:8000/chatbot/message"
headers = {
    "Content-Type": "application/json"
}

# Test Case 1: Valid Payload
print("--- Test Case 1: Valid Payload ---")
payload1 = {
    "message": "Hello",
    "session_id": "anon-session"
}
try:
    response = requests.post(url, json=payload1, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Test Case 2: Missing session_id
print("\n--- Test Case 2: Missing session_id ---")
payload2 = {
    "message": "Hello"
}
try:
    response = requests.post(url, json=payload2, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Test Case 3: Empty Payload
print("\n--- Test Case 3: Empty Payload ---")
payload3 = {}
try:
    response = requests.post(url, json=payload3, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Test Case 4: Malformed JSON (String instead of dict)
# requests.post(json=...) automatically makes it a dict, so we use data=...
print("\n--- Test Case 4: Malformed JSON ---")
try:
    response = requests.post(url, data="not a json", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
=======
BASE_URL = "http://127.0.0.1:8000"

def test_upload():
    # 1. Register/Login
    username = "testuser_repro"
    email = "test_repro@example.com"
    password = "password123"

    print(f"Registering {email}...")
    resp = requests.post(f"{BASE_URL}/auth/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    
    if resp.status_code == 201:
        print("Registered.")
    elif resp.status_code == 400 and "Email already registered" in resp.text:
        print("User already exists, logging in...")
    else:
        print(f"Registration failed: {resp.text}")
        # Try login anyway

    print("Logging in...")
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return

    token = resp.json()["access_token"]
    print(f"Got token: {token[:10]}...")

    # 2. Upload Resume
    print("Uploading resume...")
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": ("resume.txt", "This is a test resume content for debugging purposes.", "text/plain")}
    
    resp = requests.post(f"{BASE_URL}/resume/upload", headers=headers, files=files)
    
    print(f"Upload Status: {resp.status_code}")
    print(f"Upload Response: {resp.text}")

if __name__ == "__main__":
    try:
        test_upload()
    except Exception as e:
        print(f"Error: {e}")
>>>>>>> 50bca5e (Comprehensive project update: All feature modifications, new cheating detection modules, diagnostic scripts, and verification tools)
