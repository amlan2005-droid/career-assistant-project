import re
from typing import Dict, List


# -------------------------------------------------
# Canonical Skill Dictionary
# -------------------------------------------------
# key   = normalized skill name
# value = list of exact keywords / aliases
# -------------------------------------------------
SKILL_KEYWORDS: Dict[str, List[str]] = {
    # Backend
    "python": ["python"],
    "java": ["java"],
    "fastapi": ["fastapi"],
    "django": ["django"],
    "flask": ["flask"],
    "spring boot": ["spring boot", "springboot"],
    "jdbc": ["jdbc"],
    "hibernate": ["hibernate"],

    # Frontend
    "react": ["react", "react.js"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript"],
    "html": ["html"],
    "css": ["css"],

    # DevOps / Cloud
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "ec2", "s3", "lambda"],
    "jenkins": ["jenkins"],
    "ci/cd": ["ci/cd", "continuous integration", "continuous deployment"],

    # Databases
    "sql": ["sql"],
    "postgresql": ["postgresql", "postgres"],
    "mysql": ["mysql"],

    # ML / AI
    "machine learning": ["machine learning"],
    "deep learning": ["deep learning"],
    "nlp": ["nlp", "natural language processing"],
}


# -------------------------------------------------
# Normalize text
# -------------------------------------------------
def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s+/.-]", " ", text)
    return text


# -------------------------------------------------
# Layer 1: Raw Skill Extraction (STRICT)
# -------------------------------------------------
def extract_raw_skills(resume_text: str) -> Dict[str, List[str]]:
    """
    Returns:
    {
        "python": ["python"],
        "docker": ["docker"],
        "aws": ["ec2", "s3"]
    }
    """
    normalized_text = normalize_text(resume_text)
    found_skills: Dict[str, List[str]] = {}

    for skill, keywords in SKILL_KEYWORDS.items():
        matched_keywords = []

        for kw in keywords:
            # Exact / word-boundary match
            pattern = r"\b" + re.escape(kw.lower()) + r"\b"
            if re.search(pattern, normalized_text):
                matched_keywords.append(kw)

        if matched_keywords:
            found_skills[skill] = matched_keywords

    return found_skills


# -------------------------------------------------
# Utility: Flatten skills (for compatibility)
# -------------------------------------------------
def flatten_skills(skill_map: Dict[str, List[str]]) -> List[str]:
    """
    Converts:
    {"python": ["python"], "docker": ["docker"]}
    → ["python", "docker"]
    """
    return list(skill_map.keys())
