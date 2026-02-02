from app.services.resume_parser import extract_features
from app.services.reasoning_service import generate_reasoned_feedback

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
    
    # 🔍 DEBUG: Print extracted skills to see what's being found
    print(f"🔍 DEBUG - Extracted skills: {features['skills']}")
    print(f"🔍 DEBUG - Resume text preview: {resume_text[:200]}...")


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
    if features["metrics_count"] >= 8:
        strengths.append(f"Excellent quantified impact with {features['metrics_count']} measurable achievements")
    elif features["metrics_count"] >= 5:
        strengths.append(f"Strong use of metrics ({features['metrics_count']} quantified results)")
    elif features["metrics_count"] >= 3:
        strengths.append("Good quantified achievements")
    
    # Skills-based strengths
    if features["skills_count"] >= 20:
        strengths.append(f"Comprehensive skillset ({features['skills_count']} skills listed)")
    elif features["skills_count"] >= 15:
        strengths.append("Broad technical expertise")
    elif features["skills_count"] >= 10 and skills_pct > 60:
        strengths.append("Well-rounded technical skills")
    
    # Projects-based strengths
    if features["projects_count"] >= 5:
        strengths.append(f"Impressive portfolio ({features['projects_count']} projects)")
    elif features["projects_count"] >= 3:
        strengths.append("Solid hands-on project experience")
    
    # Experience-based strengths
    if features["experience_years"] >= 5:
        strengths.append(f"Extensive experience ({features['experience_years']}+ years)")
    elif features["experience_years"] >= 2:
        strengths.append("Good professional experience")
    
    # ADI-based strengths
    if adi_score >= 8:
        strengths.append("High achievement density throughout")
    
    # Fluff-based strength
    if features["fluff_phrases_count"] <= 2:
        strengths.append("Concise, professional language")

    # ---------- Dynamic Weaknesses ----------
    weaknesses = []
    
    # Find the weakest area
    component_scores = {
        "achievements": achievements_pct,
        "projects": projects_pct,
        "skills": skills_pct
    }
    weakest = min(component_scores, key=component_scores.get)
    
    # Achievements weaknesses
    if features["metrics_count"] == 0:
        weaknesses.append("No quantified achievements - add specific numbers and results")
    elif features["metrics_count"] <= 2 and weakest == "achievements":
        weaknesses.append("Limited measurable outcomes - quantify your impact more")
    
    # Projects weaknesses
    if features["projects_count"] == 0:
        weaknesses.append("No projects listed - add practical work examples")
    elif features["projects_count"] == 1:
        weaknesses.append("Only one project shown - add more to demonstrate breadth")
    elif features["projects_count"] <= 2 and weakest == "projects":
        weaknesses.append("Limited project portfolio")
    
    # Skills weaknesses
    if features["skills_count"] < 5:
        weaknesses.append("Very limited skills listed - expand technical competencies")
    elif features["skills_count"] < 8 and weakest == "skills":
        weaknesses.append("Narrow skill range - broaden technical expertise")
    
    # Fluff weaknesses
    if features["fluff_phrases_count"] > 8:
        weaknesses.append(f"Excessive generic phrases ({features['fluff_phrases_count']} found) - be more specific")
    elif features["fluff_phrases_count"] > 5:
        weaknesses.append("Too many vague statements - use concrete examples")
    
    # ADI weaknesses
    if adi_score < 2 and features["metrics_count"] > 0:
        weaknesses.append("Low achievement density - spread metrics throughout resume")
    
    # Experience weaknesses (for freshers)
    if features["experience_years"] < 1 and features["projects_count"] < 3:
        weaknesses.append("Limited experience - compensate with more projects")

    # ---------- Dynamic Suggestions ----------
    suggestions = []
    
    # Prioritize suggestions based on what needs most improvement
    if achievements_pct < 40:
        if features["metrics_count"] == 0:
            suggestions.append("Add numbers to every accomplishment (e.g., 'Increased efficiency by 30%')")
        else:
            suggestions.append(f"Add {5 - features['metrics_count']} more quantified achievements")
    
    if projects_pct < 50:
        if features["projects_count"] < 2:
            suggestions.append("Add at least 2-3 real-world projects with technical details")
        else:
            suggestions.append("Expand project descriptions with tech stack and outcomes")
    
    if skills_pct < 50:
        suggestions.append(f"List {12 - features['skills_count']} more relevant technical skills")
    
    if features["fluff_phrases_count"] > 4:
        suggestions.append("Replace generic phrases with specific, measurable contributions")
    
    if adi_score < 5 and features["metrics_count"] >= 3:
        suggestions.append("Better distribute achievements across all experiences")
    
    if features["experience_years"] < 1:
        suggestions.append("Highlight internships, academic projects, and certifications")
    
    # Add role-specific suggestions based on experience level
    if features["experience_years"] >= 3 and features["metrics_count"] < 5:
        suggestions.append("With your experience, emphasize leadership and measurable impact")
    
    # Ensure we have at least some feedback
    if not strengths:
        strengths.append("Resume submitted for analysis")
    if not weaknesses:
        weaknesses.append("Consider adding more quantified achievements")
    if not suggestions:
        suggestions.append("Focus on highlighting measurable outcomes")

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
        "resume_score": resume_score,
        "score": resume_score,  # Alias for frontend
        "experience_level": "Fresher" if features["experience_years"] < 1 else "Experienced",
        "experience_years": features["experience_years"],  # Alias for frontend
        "skills": features["skills"],
        "skills_found": features["skills"],  # Alias for frontend
        "skill_insights": skill_insights, # Added for frontend visualization
        "education": features["education_level"],  # Alias for frontend
        "projects_count": features["projects_count"],
        "strengths": strengths[:3],
        "weaknesses": weaknesses[:3],
        "suggestions": suggestions[:3],
        "achievement_density_index": {
            "adi_score": adi_score,
            "metrics_found": features["metrics_count"]
        }
    }
    
    # Enhance with AI reasoning (Gemini refines the feedback)
    try:
        ai_feedback = generate_reasoned_feedback(resume_data)
        
        # Use AI feedback if valid, fallback to rule-based if AI fails
        if ai_feedback and all(key in ai_feedback for key in ["strengths", "weaknesses", "suggestions"]):
            resume_data["strengths"] = ai_feedback["strengths"][:3] if ai_feedback["strengths"] else strengths[:3]
            resume_data["weaknesses"] = ai_feedback["weaknesses"][:3] if ai_feedback["weaknesses"] else weaknesses[:3]
            resume_data["suggestions"] = ai_feedback["suggestions"][:3] if ai_feedback["suggestions"] else suggestions[:3]
    except Exception as e:
        # Keep rule-based feedback on any error
        pass
    
    return resume_data
