from app.services.interview_engine import generate_resume_aware_questions
from unittest.mock import patch

def test_fallback_deduplication():
    print("\n--- Testing Interview Fallback Deduplication ---")
    
    # Mock resume profile
    class MockProfile:
        def __init__(self, skills):
            self.skills = skills

    # Test Case 1: Overlapping domain and skills (Repetitive case)
    print("Testing overlapping domain and skills...")
    domain = "DevOps"
    profile = MockProfile(["AWS", "DevOps", "Docker"])
    
    with patch('app.services.interview_engine.ask_gemini', return_value="ERROR: Empty response from Gemini"):
        questions = generate_resume_aware_questions(domain, profile)
        print(f"Fallback Question: {questions[0]}")
        assert "DevOps and tools like" in questions[0]
        # Verify DevOps is not repeated in the "tools like" section
        assert "DevOps and tools like AWS, Docker" in questions[0]
        assert "DevOps, AWS" not in questions[0]
        print("✅ Case 1 Passed")

    # Test Case 2: No overlapping skills
    print("\nTesting no overlapping skills...")
    domain = "Backend"
    profile = MockProfile(["Python", "FastAPI"])
    
    with patch('app.services.interview_engine.ask_gemini', return_value="ERROR: Empty response from Gemini"):
        questions = generate_resume_aware_questions(domain, profile)
        print(f"Fallback Question: {questions[0]}")
        assert "Backend and tools like Python, FastAPI" in questions[0]
        print("✅ Case 2 Passed")

    # Test Case 3: Empty skills list
    print("\nTesting empty skills list...")
    domain = "HR"
    profile = MockProfile([])
    
    with patch('app.services.interview_engine.ask_gemini', return_value="ERROR: Empty response from Gemini"):
        questions = generate_resume_aware_questions(domain, profile)
        print(f"Fallback Question: {questions[0]}")
        assert "Tell me about your experience with HR." in questions[0]
        assert "tools like" not in questions[0]
        print("✅ Case 3 Passed")

if __name__ == "__main__":
    test_fallback_deduplication()
