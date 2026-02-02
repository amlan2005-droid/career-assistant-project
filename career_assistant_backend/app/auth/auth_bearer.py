from fastapi import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional

from app.auth.auth_handler import decode_jwt  # make sure this exists
from pydantic import BaseModel


class AuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(AuthBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        # Log headers to debug 403
        print(f"DEBUG Headers: {request.headers}")
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)
        if credentials is None:
             raise HTTPException(status_code=401, detail="Authentication credentials missing")
        if credentials.scheme != "Bearer":
             raise HTTPException(status_code=401, detail="Invalid authentication scheme. Bearer token required.")
        
        error_msg = self.verify_jwt(credentials.credentials)
        if error_msg:
             raise HTTPException(status_code=401, detail=f"Invalid or expired token: {error_msg}")
        return credentials

    def verify_jwt(self, jwtoken: str) -> Optional[str]:
        try:
            payload = decode_jwt(jwtoken)
            if not payload:
                return "Payload is empty or decode failed (check server logs)"
        except Exception as e:
            return str(e)
        return None


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

