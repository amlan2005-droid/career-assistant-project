import requests

BASE_URL = "http://127.0.0.1:8000"

def test_duplicate_username():
    # Attempt to register with the same username but different email
    username = "DemoUser"
    email = "user_new@example.com"
    password = "string"

    print(f"Attempting to register {email} with existing username '{username}'...")
    resp = requests.post(f"{BASE_URL}/auth/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    
    print(f"Status Code: {resp.status_code}")
    try:
        print(f"Response JSON: {resp.json()}")
    except:
        print(f"Response Text: {resp.text}")

if __name__ == "__main__":
    test_duplicate_username()
