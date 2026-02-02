"""
Test the /interview/domains endpoint directly
"""
import requests

# Test without authentication first to see the error
try:
    response = requests.get("http://localhost:8000/interview/domains")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# If you have a token, test with it
print("\n--- If you have an auth token, the endpoint needs it ---")
print("The endpoint requires: Authorization: Bearer <token>")
