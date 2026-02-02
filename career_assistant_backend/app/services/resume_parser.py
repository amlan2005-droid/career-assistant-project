import re

ACTION_VERBS = [
    "achieved", "improved", "increased", "reduced", "optimized",
    "led", "designed", "implemented", "developed", "automated"
]

FLUFF_PHRASES = [
    "responsible for", "worked on", "basic knowledge",
    "familiar with", "helped with"
]

# Comprehensive skill list for extraction
SKILL_PATTERNS = r"\b(python|java|javascript|typescript|c\+\+|c#|ruby|php|go|rust|kotlin|swift|scala|r|matlab|" \
                r"react|angular|vue|svelte|nextjs|nuxt|django|flask|fastapi|spring|springboot|express|nestjs|" \
                r"nodejs|node\.js|deno|" \
                r"sql|mysql|postgresql|mongodb|redis|cassandra|dynamodb|oracle|sqlite|mariadb|" \
                r"docker|kubernetes|jenkins|gitlab|github|circleci|travis|terraform|ansible|" \
                r"aws|azure|gcp|heroku|vercel|netlify|digitalocean|" \
                r"git|svn|mercurial|" \
                r"html|css|sass|scss|tailwind|bootstrap|material-ui|" \
                r"graphql|rest|grpc|websocket|" \
                r"tensorflow|pytorch|keras|scikit-learn|pandas|numpy|" \
                r"agile|scrum|kanban|devops|ci/cd|tdd|bdd|" \
                r"linux|unix|windows|macos|bash|powershell|" \
                r"elasticsearch|kafka|rabbitmq|nginx|apache|" \
                r"junit|pytest|jest|mocha|cypress|selenium)\b"

def extract_features(text: str) -> dict:
    text_lower = text.lower()

    # ✅ COMPREHENSIVE REGEX SKILL EXTRACTION WITH FREQUENCY COUNTING
    skill_matches = re.findall(SKILL_PATTERNS, text_lower, re.IGNORECASE)
    
    # Count frequency of each skill
    from collections import Counter
    skill_freq = Counter(skill_matches)
    
    # Calculate confidence scores (0-1) based on frequency
    # Skills mentioned multiple times = higher confidence (primary skills)
    # Skills mentioned once = lower confidence (contextual/secondary)
    max_freq = max(skill_freq.values()) if skill_freq else 1
    skill_confidence = {
        skill: min(freq / max_freq, 1.0) 
        for skill, freq in skill_freq.items()
    }
    
    # Filter skills by confidence threshold (0.4 = mentioned at least 40% as often as top skill)
    # This removes one-off mentions while keeping important skills
    CONFIDENCE_THRESHOLD = 0.3
    primary_skills = [
        skill for skill, conf in skill_confidence.items() 
        if conf >= CONFIDENCE_THRESHOLD
    ]
    
    # Keep all skills for internal use, but mark primary ones
    all_skills = list(set(skill_matches))
    
    # 🔍 DEBUG: Print skill frequencies
    print(f"🔍 Skill frequencies: {dict(skill_freq)}")
    print(f"🔍 Primary skills (confidence >= {CONFIDENCE_THRESHOLD}): {primary_skills}")


    # projects
    projects_count = len(re.findall(r"\bproject\b", text_lower))

    # experience years
    exp_matches = re.findall(r"(\d+)\+?\s+years", text_lower)
    experience_years = max(map(int, exp_matches)) if exp_matches else 0

    # quantified achievements
    metrics_count = len(re.findall(r"\b\d+%|\b\d+\b", text))

    # action verbs
    action_verbs_count = sum(text_lower.count(v) for v in ACTION_VERBS)

    # fluff
    fluff_count = sum(text_lower.count(p) for p in FLUFF_PHRASES)

    # education
    if "phd" in text_lower:
        education_level = "phd"
    elif "master" in text_lower:
        education_level = "master"
    elif "bachelor" in text_lower:
        education_level = "bachelor"
    else:
        education_level = "other"

    return {
        "skills": primary_skills,  # ✅ Return only high-confidence primary skills
        "all_skills": all_skills,  # Keep all for internal analysis
        "skill_confidence": skill_confidence,  # Confidence scores for each skill
        "skills_count": len(primary_skills),
        "projects_count": projects_count,
        "experience_years": experience_years,
        "metrics_count": metrics_count,
        "action_verbs_count": action_verbs_count,
        "fluff_phrases_count": fluff_count,
        "education_level": education_level
    }
