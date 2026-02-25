import requests

BASE_URL = "http://127.0.0.1:8000"

def test_email_casing():
    # Login with different casing
    email = "USER@EXAMPLE.COM"
    password = "string"

    print(f"Attempting login for {email}...")
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    
    print(f"Status Code: {resp.status_code}")
    if resp.status_code == 200:
        print("Success: Login works with different casing.")
    else:
        print(f"Failed: {resp.text}")

if __name__ == "__main__":
    test_email_casing()
