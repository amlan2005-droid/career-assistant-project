from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.resume_text_extractor import extract_text_from_resume
from app.services.resume_analysis_service import analyze_resume_text
from app.services.resume_profile_service import save_or_update_resume_profile, save_or_update_resume_analysis
from app.services.resume_analysis_service import infer_domains_from_skills
from app.auth.dependencies import get_db, get_current_user
from app.models.resume_insights import ResumeInsights

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Upload a PDF or DOCX resume, extract text (OCR if scanned), and analyze it.
    """
    # Read file bytes
    file_bytes = await file.read()

    # Extract text from resume
    text, is_scanned = extract_text_from_resume(file_bytes, file.filename)

    # If no meaningful text found
    if len(text.strip()) < 50:
        raise HTTPException(
            status_code=422,
            detail="Unable to extract meaningful text. Resume may be scanned or image-only."
        )

    # Analyze text (works for both scanned and normal)
    analysis = analyze_resume_text(text)

    # Save to ResumeProfile table
    save_or_update_resume_profile(
        db=db,
        user_id=current_user.id,
        analysis=analysis
    )
    
    # Save to ResumeAnalysis table with inferred domains
    save_or_update_resume_analysis(
        db=db,
        user_id=current_user.id,
        analysis=analysis
    )
    
    # ✅ STEP 3: Save domains to ResumeInsights table using new function
    skills = analysis.get("skills", [])
    domains = infer_domains_from_skills(skills)
    
    # Check if ResumeInsights already exists for this user
    existing_insights = db.query(ResumeInsights).filter(
        ResumeInsights.user_id == current_user.id
    ).first()
    
    if existing_insights:
        # Update existing record
        existing_insights.domains = ",".join(domains)
        existing_insights.skills = ",".join(skills)
    else:
        # Create new record
        resume_insight = ResumeInsights(
            user_id=current_user.id,
            domains=",".join(domains),
            skills=",".join(skills)
        )
        db.add(resume_insight)
    
    db.commit()

    message = "Resume analyzed successfully."
    if is_scanned:
        message = "Resume extracted via OCR (scanned PDF)."

    return {
        "message": message,
        "is_scanned": is_scanned,
        "analysis": analysis
    }
