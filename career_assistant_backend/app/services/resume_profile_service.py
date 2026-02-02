from sqlalchemy.orm import Session
from app.models.resume_profile import ResumeProfile
from app.models.resume_analysis import ResumeAnalysis
from app.services.resume_analysis_service import infer_domains_from_skills

def save_or_update_resume_analysis(db: Session, user_id: int, analysis: dict):
    """
    Save or update resume analysis with inferred domains.
    """
    # Infer domains from skills using the new comprehensive function
    skills = analysis.get("skills", [])
    domains = infer_domains_from_skills(skills)
    
    # Check if analysis already exists
    resume_analysis = db.query(ResumeAnalysis).filter(
        ResumeAnalysis.user_id == user_id
    ).first()
    
    if resume_analysis:
        # Update existing record
        resume_analysis.domains = domains
        resume_analysis.skills = skills
        resume_analysis.experience_level = analysis.get("experience_level", "")
        resume_analysis.resume_score = analysis.get("resume_score", 0)
        resume_analysis.strengths = analysis.get("strengths", [])
        resume_analysis.weaknesses = analysis.get("weaknesses", [])
        resume_analysis.suggestions = analysis.get("suggestions", [])
        resume_analysis.achievement_density = analysis.get("achievement_density_index", {})
        resume_analysis.skill_insights = analysis.get("skill_insights", [])
    else:
        # Create new record
        resume_analysis = ResumeAnalysis(
            user_id=user_id,
            domains=domains,
            skills=skills,
            experience_level=analysis.get("experience_level", ""),
            resume_score=analysis.get("resume_score", 0),
            strengths=analysis.get("strengths", []),
            weaknesses=analysis.get("weaknesses", []),
            suggestions=analysis.get("suggestions", []),
            achievement_density=analysis.get("achievement_density_index", {}),
            skill_insights=analysis.get("skill_insights", [])
        )
        db.add(resume_analysis)
    
    db.commit()
    return resume_analysis

def save_or_update_resume_profile(db: Session, user_id: int, analysis: dict):
    profile = db.query(ResumeProfile).filter(
        ResumeProfile.user_id == user_id
    ).first()

    if profile:
        profile.skills = analysis.get("skills", [])
        profile.projects = analysis.get("projects", []) # Parser currently doesn't return list
        profile.strengths = analysis.get("strengths", [])
        profile.weaknesses = analysis.get("weaknesses", [])
    else:
        profile = ResumeProfile(
            user_id=user_id,
            skills=analysis.get("skills", []),
            projects=analysis.get("projects", []),
            strengths=analysis.get("strengths", []),
            weaknesses=analysis.get("weaknesses", [])
        )
        db.add(profile)

    db.commit()
    return profile


def get_resume_profile(db: Session, user_id: int):
    return db.query(ResumeProfile).filter(
        ResumeProfile.user_id == user_id
    ).first()
