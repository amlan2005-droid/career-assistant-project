import re
from typing import Dict, List


# -----------------------------------------
# Resume Section Patterns
# -----------------------------------------
SECTION_PATTERNS = {
    "experience": r"(experience|work history|employment)",
    "projects": r"(projects|project experience)",
    "certifications": r"(certifications|certified|certificate)",
    "skills": r"(skills|technical skills|tech stack)",
    "education": r"(education|academic)",
    "tools": r"(tools|technologies|tooling)",
}


# -----------------------------------------
# Split resume into sections
# -----------------------------------------
def split_into_sections(resume_text: str) -> Dict[str, str]:
    text = resume_text.lower()
    sections = {}
    current_section = "other"
    sections[current_section] = ""

    for line in text.splitlines():
        for section, pattern in SECTION_PATTERNS.items():
            if re.search(pattern, line):
                current_section = section
                sections[current_section] = ""
                break

        sections[current_section] += line + "\n"

    return sections


# -----------------------------------------
# Analyze skill context
# -----------------------------------------
def analyze_skill_context(
    resume_text: str,
    extracted_skills: Dict[str, List[str]]
) -> Dict[str, Dict]:
    """
    Returns:
    {
        "docker": {
            "contexts": ["experience", "projects"],
            "mentions": 3,
            "confidence": 0.85
        }
    }
    """
    sections = split_into_sections(resume_text)
    results = {}

    for skill, keywords in extracted_skills.items():
        contexts = set()
        mention_count = 0

        for section, content in sections.items():
            for kw in keywords:
                pattern = r"\b" + re.escape(kw.lower()) + r"\b"
                matches = re.findall(pattern, content)
                if matches:
                    contexts.add(section)
                    mention_count += len(matches)

        confidence = calculate_confidence(contexts, mention_count)

        results[skill] = {
            "contexts": sorted(list(contexts)),
            "mentions": mention_count,
            "confidence": confidence
        }

    return results


# -----------------------------------------
# Confidence scoring logic
# -----------------------------------------
def calculate_confidence(contexts: set, mentions: int) -> float:
    score = 0.0

    if "experience" in contexts:
        score += 0.45
    if "projects" in contexts:
        score += 0.30
    if "certifications" in contexts:
        score += 0.20
    if "skills" in contexts:
        score += 0.10
    if "education" in contexts:
        score += 0.10

    score += min(mentions * 0.05, 0.20)

    return round(min(score, 1.0), 2)
