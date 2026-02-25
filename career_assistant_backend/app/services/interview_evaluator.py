import json
import re
from app.services.gemini_client import ask_gemini


def evaluate_answer(answer, question, difficulty):
    strictness = {
        "easy": "lenient, focus on understanding basic concepts",
        "medium": "balanced, expects real-world application examples",
        "hard": "strict, expects deep technical insights and precision"
    }

    style = strictness.get(difficulty, "balanced")

    prompt = f"""
You are a strict technical interviewer. Evaluate the candidate's answer based on technical accuracy, depth, and clarity.

Scoring Rules (MANDATORY):
- 9–10: EXCELLENT. Production-level understanding, detailed explanation, and practical examples.
- 7–8: GOOD. Correct answer but missing some depth, edge cases, or minor details.
- 5–6: AVERAGE. Partially correct or vague. Demonstrates only surface-level knowledge.
- 3–4: POOR. Mostly incorrect or significantly lacks understanding of core concepts.
- 0–2: FAIL. Wrong, irrelevant, or "I don't know" style answers.

CRITICAL:
- DO NOT default to 6.
- Be strict.

Question: {question}
Answer: {answer}
Difficulty: {difficulty}

Evaluation style:
{style}

Return ONLY a JSON object with:
- score (0–10)
- skill
- confidence (0.0–1.0)
- strength
- weakness
- feedback
"""

    response_text = ask_gemini(prompt)

    try:
        code_block_match = re.search(
            r'```(?:json)?\s*(\{.*?\})\s*```',
            response_text,
            re.DOTALL | re.IGNORECASE
        )
        if code_block_match:
            return json.loads(code_block_match.group(1))

        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))

        print("FAILED TO PARSE JSON:", response_text)
        return {
            "score": 2,
            "skill": "unknown",
            "confidence": 0.1,
            "strength": "N/A",
            "weakness": "Evaluation failed",
            "feedback": "AI response format invalid."
        }

    except Exception as e:
        print("EVALUATION ERROR:", e, response_text)
        return {
            "score": 2,
            "skill": "unknown",
            "confidence": 0.1,
            "strength": "N/A",
            "weakness": "Evaluation failed",
            "feedback": "AI response processing error."
        }


def apply_cheating_penalty(score, warnings, terminated):
    """
    Apply penalty to the technical score based on cheating violations.
    """
    if terminated:
        return 0

    penalty = warnings * 5
    return max(score - penalty, 0)


def finalize_interview(session_id: str) -> dict:
    """
    Final score = Answer score – cheating penalty
    """

    # MOCK DATA (replace with DB later)
    ai_score = 85  # aggregated score from answers
    cheating_stats = {
        "tab_switches": 4,
        "face_missing_seconds": 18,
        "multiple_faces_detected": 0,
        "gaze_away_events": 6
    }

    penalty_result = calculate_cheating_penalty(cheating_stats)

    final_score = max(ai_score - penalty_result["penalty"], 0)

    integrity_status = (
        "High Risk" if penalty_result["penalty"] >= 30
        else "Moderate Risk" if penalty_result["penalty"] >= 15
        else "Clean"
    )

    return {
        "final_score": final_score,
        "ai_score": ai_score,
        "cheating_penalty": penalty_result["penalty"],
        "cheating_reasons": penalty_result["reasons"],
        "integrity_status": integrity_status,
        "feedback": generate_final_feedback(final_score, integrity_status)
    }


def generate_final_feedback(score: int, integrity_status: str) -> str:
    if integrity_status == "High Risk":
        return "Your technical performance was affected by integrity violations during the interview."

    if score >= 80:
        return "Strong performance with good technical understanding."
    elif score >= 60:
        return "Decent performance but needs improvement in depth."
    else:
        return "Performance did not meet expectations. Review fundamentals."


def calculate_cheating_penalty(cheating_stats: dict) -> dict:
    penalty = 0
    reasons = []

    if cheating_stats.get("tab_switches", 0) >= 3:
        penalty += 10
        reasons.append("Excessive tab switching")

    if cheating_stats.get("face_missing_seconds", 0) > 15:
        penalty += 15
        reasons.append("Face not visible for long duration")

    if cheating_stats.get("multiple_faces_detected", 0) > 0:
        penalty += 25
        reasons.append("Multiple faces detected")

    if cheating_stats.get("gaze_away_events", 0) > 5:
        penalty += 10
        reasons.append("Frequent gaze away from screen")

    return {
        "penalty": min(penalty, 40),  # cap penalty
        "reasons": reasons
    }
