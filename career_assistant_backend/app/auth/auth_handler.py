import os
from datetime import datetime, timedelta, timezone
from typing import Union, Dict
from jose import JWTError, jwt, ExpiredSignatureError

# SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
SECRET_KEY = "SUPER_FIXED_KEY_123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080 # 7 days
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    print(f"DEBUG: Signing with key='{SECRET_KEY[:3]}...' Algo={ALGORITHM}")
    expire_delta = expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expire_delta
    print(f"DEBUG: Token will expire at: {expire} (in {expire_delta})")
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt(token: str) -> Dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except ExpiredSignatureError:
        print("DEBUG: Token has expired.")
        raise
    except JWTError as e:
        print(f"DEBUG: Decode failed. Error: {e}")
        raise
