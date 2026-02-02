import requests

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
