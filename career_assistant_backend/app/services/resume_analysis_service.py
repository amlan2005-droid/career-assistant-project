from app.services.resume_parser import extract_features
from app.services.reasoning_service import generate_reasoned_feedback
import random

# ---------- SKILL TO DOMAIN MAPPING ----------

SKILL_DOMAIN_MAP = {
    "Spring Boot": "java-backend",
    "Servlet": "java-backend",
    "JDBC": "java-backend",
    "FastAPI": "python-backend",
    "Django": "python-backend",
    "Docker": "devops",
    "Kubernetes": "devops",
    "CI/CD": "devops"
}

def infer_domains(skills: list[str]) -> list[str]:
    """
    Infer domains from a list of skills using the SKILL_DOMAIN_MAP.
    
    Args:
        skills: List of skill strings
        
    Returns:
        List of unique domain strings (e.g., ["java-backend", "devops"])
    """
    domains = set()
    for skill in skills:
        if skill in SKILL_DOMAIN_MAP:
            domains.add(SKILL_DOMAIN_MAP[skill])
    return list(domains)


def infer_domains_from_skills(skills: list[str]) -> list[str]:
    """
    Infer domains from skills using pattern matching.
    More comprehensive than the simple map-based approach.
    
    Args:
        skills: List of skill strings
        
    Returns:
        List of unique domain strings
    """
    skills = [s.lower() for s in skills]
    domains = set()

    java = {"java", "spring", "spring boot", "jdbc", "hibernate"}
    python = {"python", "fastapi", "django", "flask"}
    devops = {"docker", "kubernetes", "ci/cd", "jenkins", "aws"}
    ml = {"machine learning", "deep learning", "nlp"}

    if any(s in skills for s in java):
        domains.add("java-backend")

    if any(s in skills for s in python):
        domains.add("python-backend")

    if any(s in skills for s in devops):
        domains.add("devops")

    if any(s in skills for s in ml):
        domains.add("machine-learning")

    return list(domains)

# ---------- SCORING FUNCTIONS (SMOOTHED) ----------

def score_skills(count):
    # More gradual increase, rewards 10-20 skills optimally
    if count < 5:
        return count * 2
    elif count < 15:
        return 10 + (count - 5) * 1.5
    else:
        return min(25, 25 + (count - 15) * 0.3)


def score_projects(count):
    # Rewards 2-5 projects well
    if count == 0:
        return 0
    elif count == 1:
        return 8
    elif count <= 3:
        return 8 + (count - 1) * 6
    else:
        return min(20, 20 + (count - 3) * 1)


def score_experience(years):
    # Better curve for 0-10 years
    if years < 1:
        return 0
    elif years <= 5:
        return years * 4
    else:
        return min(20, 20 + (years - 5) * 0.5)


def score_achievements(metrics):
    # Strong emphasis on quantified achievements
    if metrics == 0:
        return 0
    elif metrics <= 3:
        return metrics * 6
    elif metrics <= 8:
        return 18 + (metrics - 3) * 4
    else:
        return min(30, 38 + (metrics - 8) * 1)


def score_education(level):
    weights = {
        "phd": 8,
        "master": 6,
        "bachelor": 4,
        "other": 2
    }
    return weights.get(level, 2)


def penalty_fluff(count):
    # Stronger penalty for fluff
    if count <= 2:
        return count * 0.5
    elif count <= 5:
        return 1 + (count - 2) * 2
    else:
        return min(15, 7 + (count - 5) * 2)


def normalize(score, max_score=115):
    # Adjusted max score for new weights
    score = max(0, min(score, max_score))
    return round((score / max_score) * 100)


# ---------- MAIN ANALYSIS ----------

def analyze_resume_text(resume_text: str) -> dict:
    features = extract_features(resume_text)
    
    # DEBUG: Print extracted skills to see what's being found
    print(f"DEBUG - Extracted skills: {features['skills']}")
    print(f"DEBUG - Resume text preview: {resume_text[:200]}...")


    raw_score = (
        score_skills(features["skills_count"]) +
        score_projects(features["projects_count"]) +
        score_experience(features["experience_years"]) +
        score_achievements(features["metrics_count"]) +
        score_education(features["education_level"]) -
        penalty_fluff(features["fluff_phrases_count"])
    )

    resume_score = normalize(raw_score)

    # ---------- ADI (Achievement Density Index) ----------
    # Calculate based on achievements per 100 words (more realistic)
    word_count = len(resume_text.split())
    if word_count > 0 and features["metrics_count"] > 0:
        # Achievement density = (achievements / words) * 100
        # Good resume has ~2-5 achievements per 100 words
        achievements_per_100_words = (features["metrics_count"] / word_count) * 100
        
        # Map to 0-10 scale with realistic thresholds
        if achievements_per_100_words >= 5:
            adi_score = 10
        elif achievements_per_100_words >= 3.5:
            adi_score = 8 + (achievements_per_100_words - 3.5) * 1.3
        elif achievements_per_100_words >= 2:
            adi_score = 5 + (achievements_per_100_words - 2) * 2
        elif achievements_per_100_words >= 1:
            adi_score = 2 + (achievements_per_100_words - 1) * 3
        else:
            adi_score = achievements_per_100_words * 2
        
        adi_score = round(min(adi_score, 10), 1)
    else:
        adi_score = 0

    # ---------- Calculate Component Scores for Comparison ----------
    skills_score = score_skills(features["skills_count"])
    projects_score = score_projects(features["projects_count"])
    experience_score = score_experience(features["experience_years"])
    achievements_score = score_achievements(features["metrics_count"])
    education_score = score_education(features["education_level"])
    
    # Component scores as percentages of their max
    skills_pct = (skills_score / 25) * 100
    projects_pct = (projects_score / 20) * 100
    achievements_pct = (achievements_score / 30) * 100
    
    # ---------- Dynamic Strengths ----------
    strengths = []
    
    # Achievements-based strengths
    if features["metrics_count"] >= 5:
        strengths.append(f"Strong use of metrics ({features['metrics_count']} quantified results found)")
    elif features["metrics_count"] >= 2:
        strengths.append("Good start at quantifying professional achievements")
    
    # Skills-based strengths
    if features["skills_count"] >= 12:
        strengths.append(f"Comprehensive technical toolkit with {features['skills_count']} core skills")
    elif features["skills_count"] >= 6:
        strengths.append("Solid foundation in relevant technical competencies")
    elif features["skills_count"] > 0:
        main_skill = features["skills"][0].capitalize()
        strengths.append(f"Clear focus on {main_skill} and related technologies")
    
    # Projects-based strengths
    if features["projects_count"] >= 3:
        strengths.append(f"Active project portfolio with {features['projects_count']} distinct works")
    elif features["projects_count"] >= 1:
        strengths.append("Demonstrated hands-on experience through project work")
    
    # Experience-based strengths
    if features["experience_years"] >= 3:
        strengths.append(f"Established professional track record ({features['experience_years']} years)")
    elif features["experience_years"] > 0:
        strengths.append("Growing industry experience and professional presence")
    
    # Fluff-based strength
    if features["fluff_phrases_count"] <= 2:
        strengths.append("Clean, high-impact professional language")

    # ---------- Dynamic Weaknesses ----------
    weaknesses = []
    
    # Achievements weaknesses
    if features["metrics_count"] == 0:
        weaknesses.append("Lack of quantified impact - use percentages or numbers to show value")
    elif features["metrics_count"] < 3:
        weaknesses.append("Limited measurable data - quantify more of your accomplishments")
    
    # Projects weaknesses
    if features["projects_count"] == 0:
        weaknesses.append("Missing project section - add real-world applications of your skills")
    elif features["projects_count"] < 2:
        weaknesses.append("Single project listed - expand your portfolio to show technical breadth")
    
    # Skills weaknesses
    if features["skills_count"] < 4:
        weaknesses.append("Narrow technical range - consider listing more tangential skills")
    
    # Fluff weaknesses
    if features["fluff_phrases_count"] > 5:
        weaknesses.append(f"High generic language count ({features['fluff_phrases_count']}) - replace vague terms with action verbs")

    # ---------- Dynamic Suggestions ----------
    suggestions = []
    
    # Personalize suggestions based on missing pieces
    if features["metrics_count"] < 3:
        suggestions.append("Apply the STAR method to your bullet points to include clear metrics")
    
    if features["projects_count"] < 2:
        suggestions.append("Host a personal project on GitHub and include the link on your resume")
    
    if features["skills_count"] < 8:
        suggestions.append(f"Deepen your expertise in {features['skills'][0] if features['skills'] else 'your core domains'}")
    
    if features["fluff_phrases_count"] > 3:
        suggestions.append("Scrub generic phrases like 'responsible for' and lead with action verbs")

    # Ensure we have at least some feedback (Diversified fallbacks)
    fallback_strengths = ["Professional resume layout and structure", "Strong presentation of educational background", "Clear identification of core competencies"]
    fallback_weaknesses = ["Limited use of industry-standard action verbs", "Missing links to professional portfolio or GitHub", "Resume could be more tightly focused on specific roles"]
    fallback_suggestions = ["Incorporate more industry keywords into your summary", "Consider a modern template with better readability", "Ensure for every skill listed, you have a matching example in your experience"]

    if not strengths:
        strengths.append(random.choice(fallback_strengths))
    if not weaknesses:
        weaknesses.append(random.choice(fallback_weaknesses))
    if not suggestions:
        suggestions.append(random.choice(fallback_suggestions))

    # Calculate skill insights (High/Medium/Low confidence)
    skill_insights = []
    skill_confidence = features.get("skill_confidence", {})
    
    for skill, conf in skill_confidence.items():
        level = "low"
        if conf >= 0.7:
            level = "high"
        elif conf >= 0.4:
            level = "medium"
            
        skill_insights.append({
            "name": skill.replace("-", " ").capitalize(),
            "confidence": conf,
            "level": level
        })
    
    # Sort by confidence
    skill_insights = sorted(skill_insights, key=lambda x: x["confidence"], reverse=True)

    # Build structured data for AI reasoning
    resume_data = {
        "score": resume_score,
        "experience_level": "Fresher" if features["experience_years"] < 1 else "Experienced",
        "experience_years": features["experience_years"],
        "skills": features["skills"],
        "education": features["education_level"],
        "projects_count": features["projects_count"],
        "rule_strengths": strengths[:3],
        "rule_weaknesses": weaknesses[:3],
        "rule_suggestions": suggestions[:3],
        "achievement_density_index": {
            "adi_score": adi_score,
            "metrics_found": features["metrics_count"]
        }
    }
    
    # Enhance with AI reasoning (Gemini refines the feedback)
    try:
        ai_feedback = generate_reasoned_feedback(resume_data)
        
        # Use AI feedback if valid and NOT empty, fallback to rule-based if AI fails or returns empty lists
        if ai_feedback and any(ai_feedback.get(key) for key in ["strengths", "weaknesses", "suggestions"]):
            resume_data["strengths"] = ai_feedback.get("strengths") or strengths[:3]
            resume_data["weaknesses"] = ai_feedback.get("weaknesses") or weaknesses[:3]
            resume_data["suggestions"] = ai_feedback.get("suggestions") or suggestions[:3]
            
            # Ensure we limit to 3 items
            resume_data["strengths"] = resume_data["strengths"][:3]
            resume_data["weaknesses"] = resume_data["weaknesses"][:3]
            resume_data["suggestions"] = resume_data["suggestions"][:3]
        else:
            resume_data["strengths"] = strengths[:3]
            resume_data["weaknesses"] = weaknesses[:3]
            resume_data["suggestions"] = suggestions[:3]
    except Exception as e:
        # Keep rule-based feedback on any error
        resume_data["strengths"] = strengths[:3]
        resume_data["weaknesses"] = weaknesses[:3]
        resume_data["suggestions"] = suggestions[:3]

    # Add frontend-specific fields
    resume_data["resume_score"] = resume_score
    resume_data["skills_found"] = features["skills"]
    resume_data["skill_insights"] = skill_insights
    
    return resume_data
