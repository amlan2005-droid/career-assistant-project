from langchain_core.prompts import PromptTemplate

RESUME_ANALYSIS_PROMPT = PromptTemplate.from_template("""
You are an expert Resume Analyzer and Career Coach. 
Your task is to analyze the provided resume text and extract key professional insights.

Return the result ONLY as a JSON object with the following structure:
{{
  "skills": ["List of extracted technical and soft skills"],
  "experience_level": "One of: Fresher, Junior (1-3 yrs), Mid-Level (3-7 yrs), Senior (7+ yrs), Lead/Executive",
  "resume_score": <An integer from 0 to 100 based on quality and completeness>,
  "strengths": ["List of 2-3 key professional strengths"],
  "weaknesses": ["List of 2-3 areas for improvement"],
  "suggestions": ["List of 3-4 actionable steps to improve the resume"]
}}

Resume Text:
{resume_text}
""")
