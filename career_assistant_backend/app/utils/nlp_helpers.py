import re
import spacy

# Load spaCy's English NLP model (make sure you've installed it: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

# Example: Clean up the text
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.strip()

# Extract named entities from resume/job description
def extract_entities(text: str) -> list:
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

# Extract possible skills from resume text using a given skills list
def extract_skills(text: str, skills_list: list) -> list:
    text = clean_text(text)
    found = [skill for skill in skills_list if skill.lower() in text]
    return found

# Optional: Match job description with resume based on skills overlap
def skill_match_percentage(resume_skills: list, job_skills: list) -> float:
    if not job_skills:
        return 0.0
    matches = set(resume_skills).intersection(set(job_skills))
    return (len(matches) / len(job_skills)) * 100

