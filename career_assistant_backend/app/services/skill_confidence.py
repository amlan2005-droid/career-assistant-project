from typing import Dict, Literal

ConfidenceLevel = Literal["low", "medium", "high"]
DifficultyLevel = Literal["easy", "medium", "hard"]


# =====================================================
# Determine confidence label from numeric score
# =====================================================
def get_confidence_level(confidence_score: float) -> ConfidenceLevel:
    """
    Converts numeric confidence (0.0–1.0) to label
    """

    if confidence_score >= 0.75:
        return "high"

    if confidence_score >= 0.45:
        return "medium"

    return "low"


# =====================================================
# Map confidence → interview difficulty
# =====================================================
def map_confidence_to_difficulty(
    confidence_level: ConfidenceLevel
) -> DifficultyLevel:
    """
    Interview logic:
    - Low confidence → fundamentals
    - Medium → applied concepts
    - High → real-world & system design
    """

    mapping = {
        "low": "easy",
        "medium": "medium",
        "high": "hard"
    }

    return mapping[confidence_level]


# =====================================================
# Full skill confidence decision
# =====================================================
def evaluate_skill_confidence(skill_context: Dict) -> Dict:
    """
    Input example:
    {
        "contexts": ["experience", "projects"],
        "mentions": 4,
        "confidence": 0.82
    }

    Output:
    {
        "confidence_score": 0.82,
        "confidence_level": "high",
        "recommended_difficulty": "hard"
    }
    """

    confidence_score = skill_context.get("confidence", 0.0)

    confidence_level = get_confidence_level(confidence_score)
    difficulty = map_confidence_to_difficulty(confidence_level)

    return {
        "confidence_score": confidence_score,
        "confidence_level": confidence_level,
        "recommended_difficulty": difficulty
    }
