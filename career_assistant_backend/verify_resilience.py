
import os
import json
from unittest.mock import MagicMock, patch
from app.services.interview_engine import generate_resume_aware_questions

def test_engine_resilience():
    print("--- Testing Engine Resilience (Error Handling) ---")
    
    mock_resume = MagicMock()
    mock_resume.skills = ["Python", "Docker"]
    domain = "Backend"
    
    # CASE 1: Rate Limit Error
    print("\nCase 1: Simulate 429 Rate Limit")
    with patch('app.services.interview_engine.ask_gemini') as mock_ask:
        mock_ask.return_value = "ERROR: Rate limit exceeded. Please wait a moment."
        questions = generate_resume_aware_questions(domain, mock_resume, "medium", 5)
        print(f"Outcome: {questions[0]}")
        assert "AI is temporarily busy" in questions[0]
        assert "Rate limit exceeded" in questions[0]
        print("✅ Correctly returned fallback for 429")

    # CASE 2: Empty/Failed AI Response
    print("\nCase 2: Simulate Empty Response")
    with patch('app.services.interview_engine.ask_gemini') as mock_ask:
        mock_ask.return_value = "ERROR: Gemini failed to respond"
        questions = generate_resume_aware_questions(domain, mock_resume, "medium", 5)
        print(f"Outcome: {questions[0]}")
        assert "AI is temporarily busy" in questions[0]
        print("✅ Correctly returned fallback for failure")

    # CASE 3: Valid Response
    print("\nCase 3: Simulate Valid Response")
    with patch('app.services.interview_engine.ask_gemini') as mock_ask:
        mock_ask.return_value = "1. How do you implement robust error handling in Python applications?\n2. What is the architecture of Docker and how does it manage containers?"
        questions = generate_resume_aware_questions(domain, mock_resume, "medium", 5)
        print(f"Outcome: {questions}")
        assert len(questions) == 2
        assert "How do you implement robust" in questions[0]
        print("✅ Correctly parsed valid numbered list")

if __name__ == "__main__":
    test_engine_resilience()
