from fastapi import APIRouter

router = APIRouter()

@router.get("/mock")
def mock_questions(domain: str = "python"):
    if domain == "python":
        return {"questions": ["What is a decorator?", "Explain list comprehension."]}
    return {"questions": ["Why should we hire you?"]}
