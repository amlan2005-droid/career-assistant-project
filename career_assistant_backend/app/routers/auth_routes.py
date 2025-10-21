from fastapi import FastAPI
from app.routers import auth as auth_routes
from pydantic import BaseModel
from fastapi import APIRouter

app = FastAPI()
router = APIRouter()

# Include the auth router
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

@router.post("/register")
def register(request: RegisterRequest):
    # registration logic
    return {"message": "User registered"}
