from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
class UserRegister(BaseModel):
    username: str
    email: EmailStr  
    password: str