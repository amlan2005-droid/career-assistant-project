import os
from datetime import datetime, timedelta
from typing import Union, Dict
from jose import JWTError, jwt, ExpiredSignatureError

# SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
SECRET_KEY = "SUPER_FIXED_KEY_123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # 24 hours

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    print(f"DEBUG: Signing with key='{SECRET_KEY[:3]}...' Algo={ALGORITHM}")
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt(token: str) -> Union[Dict, None]:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except ExpiredSignatureError:
        print("DEBUG: Token has expired.")
        return None # AuthBearer will say "Invalid token" or we can return specific signal? 
        # Actually AuthBearer.verify_jwt calls decode_jwt. If nil, returns error string.
        # But verify_jwt logic (Step 294) handles None as generic "Payload empty..." unless we change decode_jwt signature or raise.
    except JWTError as e:
        print(f"DEBUG: Decode failed. Error: {e} Key='{SECRET_KEY[:3]}...'")
        return None
