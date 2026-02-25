import json
import os
from typing import Dict
from dotenv import load_dotenv
from app.services.gemini_client import ask_gemini

# Load environment variables
load_dotenv()

# ----------------------------------------------------
# SYSTEM PROMPTS
# ----------------------------------------------------
REASONING_PROMPT = """
You are a senior technical recruiter and resume evaluator.

Your task is to provide HIGHLY SPECIFIC feedback based on the provided resume data.
Avoid generic advice like "add more skills" or "use metrics". Instead, reference the actual skills and experience provided.

You MUST follow these rules strictly:
- Reason ONLY from the provided structured data (skills, experience, projects, etc.)
- Do NOT repeat the same point in different wording
- Each point must be concise, specific, and actionable
- Maximum 3 strengths, 3 weaknesses, 3 suggestions
- Suggestions must be directly tied to the technologies and experience level listed

Return ONLY valid JSON with this format:
{
  "strengths": ["specific strength 1", ...],
  "weaknesses": ["specific weakness 1", ...],
  "suggestions": ["specific suggestion 1", ...]
}
"""

SKILL_EXTRACTION_PROMPT = """
You are an expert technical recruiter analyzing a resume.

Extract ALL technical skills, tools, frameworks, and technologies mentioned in the resume.

Rules:
- Include programming languages (Python, Java, JavaScript, etc.)
- Include frameworks (React, Django, Spring Boot, etc.)
- Include tools (Docker, Git, AWS, etc.)
- Include databases (MySQL, MongoDB, PostgreSQL, etc.)
- Include methodologies (Agile, Scrum, etc.)
- Only extract skills actually mentioned in the resume
- Return skills as a simple list

Return ONLY valid JSON with this format:
{
  "skills": ["skill1", "skill2", "skill3", ...]
}
"""

# ----------------------------------------------------
# PUBLIC FUNCTIONS
# ----------------------------------------------------
def generate_reasoned_feedback(resume_data: Dict) -> Dict:
    """
    Hybrid reasoning layer.
    Uses Gemini (via gemini_client) to reason over structured resume data.
    """
    # Comprehensive input for better reasoning
    reasoning_input = {
        "score": resume_data.get("score"),
        "experience_level": resume_data.get("experience_level"),
        "experience_years": resume_data.get("experience_years", 0),
        "education": resume_data.get("education"),
        "skills_found": resume_data.get("skills", []),
        "projects_count": resume_data.get("projects_count", 0),
        "metrics_found": resume_data.get("achievement_density_index", {}).get("metrics_found", 0),
        "adi_score": resume_data.get("achievement_density_index", {}).get("adi_score", 0),
        "rule_based_strengths": resume_data.get("rule_strengths", []),
        "rule_based_weaknesses": resume_data.get("rule_weaknesses", []),
        "rule_based_suggestions": resume_data.get("rule_suggestions", [])
    }

    try:
        prompt = f"{REASONING_PROMPT}\n\nResume data to evaluate:\n{json.dumps(reasoning_input, indent=2)}\n\nIMPORTANT: Return ONLY the JSON object."
        
        response_text = ask_gemini(prompt)

        if not response_text or "ERROR:" in response_text:
            return {"strengths": [], "weaknesses": [], "suggestions": []}

        # Robust JSON extraction
        content = response_text.strip()
        start_idx = content.find('{')
        end_idx = content.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            json_str = content[start_idx:end_idx+1]
            return json.loads(json_str)
        
        return {"strengths": [], "weaknesses": [], "suggestions": []}

    except Exception as e:
        print(f"AI reasoning failed: {e}")
        return {"strengths": [], "weaknesses": [], "suggestions": []}


def extract_skills_with_ai(resume_text: str) -> list[str]:
    """
    Extract skills from resume text using Gemini (via gemini_client).
    """
    if not resume_text or len(resume_text.strip()) < 50:
        return []
    
    try:
        prompt = f"{SKILL_EXTRACTION_PROMPT}\n\nResume text:\n{resume_text[:3000]}\n\nIMPORTANT: Return ONLY the JSON object."
        
        response_text = ask_gemini(prompt)

        if not response_text or "ERROR:" in response_text:
            return []

        # Robust JSON extraction
        content = response_text.strip()
        start_idx = content.find('{')
        end_idx = content.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            json_str = content[start_idx:end_idx+1]
            result = json.loads(json_str)
            skills = result.get("skills", [])
            return [skill.strip() for skill in skills if skill.strip()]
        
        return []
        
    except Exception as e:
        print(f"AI skill extraction failed: {e}")
        return []
