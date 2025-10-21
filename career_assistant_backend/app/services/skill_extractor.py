def extract_skills(text, skills_list):
    return [skill for skill in skills_list if skill.lower() in text.lower()]
