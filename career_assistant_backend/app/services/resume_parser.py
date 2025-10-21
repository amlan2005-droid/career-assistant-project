import json

def parse_resume(file_path: str):
    """
    Parse the given resume file and extract text, entities, and skills.
    file_path: str → Path to the uploaded resume file
    """
    # 🔹 Dummy parsing logic (replace with your actual code)
    with open(file_path, "r", errors="ignore") as f:
        text = f.read()

    entities = ["Python", "FastAPI", "SQL"]
    skills = ["Problem Solving", "Backend Development"]

    parsed_data = {
        "text": text,
        "entities": entities,
        "skills": skills,
    }
    return parsed_data
