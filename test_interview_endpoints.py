import requests
import json

print("Testing /interview/domains endpoint...")
try:
    response = requests.get("http://127.0.0.1:8000/interview/domains")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

print("Testing /interview/start endpoint...")
try:
    response = requests.post(
        "http://127.0.0.1:8000/interview/start",
        json={"domain": "python"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
