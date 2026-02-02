import requests

BASE_URL = "http://127.0.0.1:8000"

def verify_login():
    email = "user@example.com"
    password = "string"

    print(f"Attempting login for {email} with password '{password}'...")
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    
    if resp.status_code == 200:
        print("Success: Login valid. Token received.")
        print(f"Token: {resp.json().get('access_token')[:10]}...")
    else:
        print(f"Failed: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    verify_login()
