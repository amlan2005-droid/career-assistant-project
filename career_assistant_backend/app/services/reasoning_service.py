import json
import os
from google import genai
from typing import Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ----------------------------------------------------
# Gemini Configuration
# ----------------------------------------------------
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ----------------------------------------------------
# SYSTEM PROMPT (STRICT CONTROL)
# ----------------------------------------------------
SYSTEM_PROMPT = """
You are a senior technical recruiter and resume evaluator.

You MUST follow these rules strictly:
- Reason ONLY from the provided structured data
- Do NOT invent skills, experience, or achievements
- Do NOT repeat the same point in different wording
- Avoid generic advice
- Each point must be concise and specific
- Maximum 3 strengths, 3 weaknesses, 3 suggestions
- Suggestions must be actionable and measurable

Return ONLY valid JSON with this format:
{
  "strengths": [],
  "weaknesses": [],
  "suggestions": []
}
"""

# ----------------------------------------------------
# PUBLIC FUNCTION
# ----------------------------------------------------
def generate_reasoned_feedback(resume_data: Dict) -> Dict:
    """
    Hybrid reasoning layer.
    Uses Gemini ONLY to reason over structured resume data.
    """

    # Minimal input (prevents hallucination)
    reasoning_input = {
        "resume_score": resume_data.get("resume_score"),
        "adi_score": resume_data.get("achievement_density_index", {}).get("adi_score"),
        "skills_count": len(resume_data.get("skills", [])),
        "projects_count": resume_data.get("projects_count", 0),
        "experience_level": resume_data.get("experience_level"),
        "metrics_count": resume_data.get("achievement_density_index", {}).get("metrics_found"),
        "rule_strengths": resume_data.get("strengths", []),
        "rule_weaknesses": resume_data.get("weaknesses", [])
    }

    try:
        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=[
                SYSTEM_PROMPT,
                f"Resume data:\n{json.dumps(reasoning_input, indent=2)}"
            ],
            config={
                "temperature": 0.25,   # low hallucination
                "top_p": 0.9,
                "max_output_tokens": 400
            }
        )

        return json.loads(response.text)

    except Exception as e:
        # Safe fallback (system never breaks)
        return {
            "strengths": [],
            "weaknesses": [],
            "suggestions": []
        }


# ----------------------------------------------------
# AI-POWERED SKILL EXTRACTION
# ----------------------------------------------------
SKILL_EXTRACTION_PROMPT = """
You are an expert technical recruiter analyzing a resume.

Extract ALL technical skills, tools, frameworks, and technologies mentioned in the resume.

Rules:
- Include programming languages (Python, Java, JavaScript, etc.)
- Include frameworks (React, Django, Spring Boot, etc.)
- Include tools (Docker, Git, AWS, etc.)
- Include databases (MySQL, MongoDB, PostgreSQL, etc.)
- Include methodologies (Agile, Scrum, etc.)
- Be comprehensive but accurate
- Only extract skills actually mentioned in the resume
- Return skills as a simple list

Return ONLY valid JSON with this format:
{
  "skills": ["skill1", "skill2", "skill3", ...]
}
"""

def extract_skills_with_ai(resume_text: str) -> list[str]:
    """
    Extract skills from resume text using Gemini AI.
    Falls back to empty list on error.
    """
    if not resume_text or len(resume_text.strip()) < 50:
        return []
    
    try:
        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=[
                SKILL_EXTRACTION_PROMPT,
                f"Resume text:\n{resume_text[:3000]}"  # Limit to first 3000 chars to avoid token limits
            ],
            config={
                "temperature": 0.1,  # Very low for factual extraction
                "top_p": 0.9,
                "max_output_tokens": 500
            }
        )
        
        result = json.loads(response.text)
        skills = result.get("skills", [])
        
        # Return list of skills (lowercase for consistency)
        return [skill.strip() for skill in skills if skill.strip()]
        
    except Exception as e:
        print(f"AI skill extraction failed: {e}")
        # Fallback to empty list
        return []
