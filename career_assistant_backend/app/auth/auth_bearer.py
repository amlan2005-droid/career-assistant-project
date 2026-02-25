from fastapi import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional

from app.auth.auth_handler import decode_jwt
from jose import ExpiredSignatureError, JWTError
from pydantic import BaseModel


class AuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(AuthBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[dict]:
        # Log headers to debug 403
        print(f"DEBUG Headers: {request.headers}")
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)
        if credentials is None:
             raise HTTPException(status_code=401, detail="Authentication credentials missing")
        if credentials.scheme != "Bearer":
             raise HTTPException(status_code=401, detail="Invalid authentication scheme. Bearer token required.")
        
        return self.verify_jwt(credentials.credentials)

    def verify_jwt(self, jwtoken: str) -> dict:
        try:
            # ✅ Fix (v2): Ultra-robust stripping of "Bearer" prefix
            # Handles "Bearer BearereyJ...", "bearer bearer eyJ...", etc.
            token_to_decode = jwtoken.strip()
            while True:
                lower_token = token_to_decode.lower()
                if lower_token.startswith("bearer "):
                    token_to_decode = token_to_decode[7:].lstrip()
                elif lower_token.startswith("bearer"):
                    token_to_decode = token_to_decode[6:].lstrip()
                else:
                    break
            
            print(f"DEBUG (v2): Final token to decode: {token_to_decode[:20]}...")
            
            payload = decode_jwt(token_to_decode)
            return payload
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired. Please log in again.")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token signature or format")
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

