import uuid
import logging
import random
import re
from app.services.gemini_client import ask_gemini

logger = logging.getLogger(__name__)

def generate_resume_aware_questions(
    domain: str, 
    resume_profile: dict, 
    difficulty: str = "medium",
    question_count: int = 5,
    previous_questions: list = None
) -> list[str]:
    """
    Generate resume-aware questions based on domain, resume profile, and difficulty.
    """
    if previous_questions is None:
        previous_questions = []
    
    DIFFICULTY_RULES = {
        "easy": {
            "style": "Foundational concepts, basic definitions, and simple use cases.",
            "complexity": "Ask what things are and how they work at a high level."
        },
        "medium": {
            "style": "Real-world application, design patterns, and common configurations.",
            "complexity": "Focus on scenario-based questions and practical problem solving."
        },
        "hard": {
            "style": "Internals, performance tuning, failure modes, and architectural trade-offs.",
            "complexity": "Ask about scaling, debugging complex issues, and edge cases where tools break."
        }
    }
    
    diff_settings = DIFFICULTY_RULES.get(difficulty, DIFFICULTY_RULES["medium"])
    
    # Extract skills
    resume_skills = resume_profile.skills if resume_profile and hasattr(resume_profile, 'skills') else []
    
    seed = random.randint(1, 1000000)
    previous_q_text = "\n- ".join(previous_questions) if previous_questions else "None"
    
    prompt = f"""
You are an expert technical recruiter and senior engineer conducting a high-stakes interview.

Domain: {domain}
Difficulty: {difficulty}
Candidate Skills: {', '.join(resume_skills) if resume_skills else 'General ' + domain + ' skills'}

RULES:
1. Generate exactly {question_count} unique interview questions.
2. SKILL INTEGRATION: Integrate skills from the candidate's list naturally into the questions. 
3. NO LABELS: Do NOT use labels like "Skill Anchor:", "Domain:", "Topic:", or any bolded headers at the start of questions.
4. FORMAT: Return the questions as a CLEAN numbered list (1., 2., ...). No intro text, no outro text, and no meta-commentary.
5. DIFFICULTY DEPTH:
   - {diff_settings['style']}
   - {diff_settings['complexity']}
6. AVOID repetition. Do not ask questions similar to these:
   - {previous_q_text}
7. Randomness Seed: {seed}

Example of GOOD natural integration:
- "In your experience with FastAPI, how do you handle asynchronous database connections to ensure optimal performance?" (Natural)
- ❌ "**Web Frameworks (Skill Anchor: FastAPI)**: How do you handle asynchronous database connections?" (Too literal/labeled)

Now, generate the {question_count} CLEAN questions:
"""

    response = ask_gemini(prompt)
    
    if response.startswith("ERROR:"):
        # Log the error and return a clear fallback
        logger.error(f"Interview generation failed: {response}")
        
        # Deduplicate skills from domain for the fallback message
        filtered_skills = [s for s in resume_skills if s.lower() != domain.lower()]
        skills_text = f" and tools like {', '.join(filtered_skills[:2])}" if filtered_skills else ""
        
        return [
            f"The AI is temporarily busy ({response.replace('ERROR: ', '')}). Let's start with a general question: Tell me about your experience with {domain}{skills_text}."
        ]

    # Parse numbered list
    questions = []
    # Match lines like "1. Question text" or "1) Question text"
    matches = re.findall(r'^\d+[\.\)]\s*(.*)', response, re.MULTILINE)
    
    if matches:
        questions = [q.strip() for q in matches]
    else:
        # Fallback if AI output is messy
        lines = [l.strip() for l in response.split('\n') if l.strip() and not l.strip().startswith('```')]
        questions = [re.sub(r'^\d+[\.\)]\s*', '', l) for l in lines]

    # Filter out short or error-like responses
    questions = [q for q in questions if len(q) > 15 and not q.startswith("ERROR:")]
    
    if not questions:
        # Ultimate fallback
        return [f"Tell me about your experience with {domain} in a production environment."]
        
    return questions[:question_count]
