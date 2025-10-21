from fastapi import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional

from app.auth.auth_handler import decode_jwt  # make sure this exists
from pydantic import BaseModel


class AuthBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)
        if credentials is None:
            raise HTTPException(status_code=403, detail="Invalid authorization credentials")
        # Add your custom validation logic here if needed
        return credentials

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decode_jwt(jwtoken)
        except:
            return False
        return True if payload else False


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

