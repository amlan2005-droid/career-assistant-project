import sys
import os
from unittest.mock import MagicMock, patch

# Add the project root to sys.path
sys.path.append(os.getcwd())

from app.services.resume_analysis_service import analyze_resume_text

def test_analyze_resume_text():
    sample_text = """
    John Doe
    Software Engineer
    
    Experience:
    - Developed a scalable web app using Python and FastAPI.
    - Increased system performance by 30% by optimizing SQL queries.
    - Led a team of 5 developers to deliver a project in 3 months.
    
    Skills: Python, FastAPI, SQL, Docker, Kubernetes.
    """
    
    # Mock LLM and get_llm
    mock_llm = MagicMock()
    mock_response = {
        "skills": ["Python", "FastAPI", "SQL", "Docker", "Kubernetes"],
        "experience_level": "Junior (1-3 yrs)",
        "resume_score": 85,
        "strengths": ["Strong technical skills", "Quantified achievements"],
        "weaknesses": ["No certifications"],
        "suggestions": ["Add certifications"]
    }
    
    with patch("app.services.resume_analysis_service.get_llm", return_value=mock_llm):
        with patch("langchain_core.prompts.PromptTemplate.invoke", return_value=None): # Not actually used like this in the chain but for safety
             with patch("langchain_core.runnables.base.RunnableSequence.invoke", return_value=mock_response):
                result = analyze_resume_text(sample_text)
                
                print("Analysis Result:")
                import json
                print(json.dumps(result, indent=2))
                
                assert "achievement_density" in result
                assert result["achievement_density"]["achievement_count"] > 0
                assert "Python" in result["skills"]
                assert "Strong quantified achievements" in result["strengths"]

if __name__ == "__main__":
    try:
        test_analyze_resume_text()
        print("\nTest Passed!")
    except Exception as e:
        print(f"\nTest Failed: {e}")
        import traceback
        traceback.print_exc()
