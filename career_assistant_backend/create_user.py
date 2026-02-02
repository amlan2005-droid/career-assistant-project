import requests

BASE_URL = "http://127.0.0.1:8000"

def create_user():
    username = "DemoUser"
    email = "user@example.com"
    password = "string"  # Matching user's input

    print(f"Registering {email} with password '{password}'...")
    resp = requests.post(f"{BASE_URL}/auth/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    
    if resp.status_code == 201:
        print("Success: User registered.")
    elif resp.status_code == 400:
        print(f"Info: {resp.json().get('detail')}")
    else:
        print(f"Failed: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    try:
        create_user()
    except Exception as e:
        print(f"Error: {e}")
