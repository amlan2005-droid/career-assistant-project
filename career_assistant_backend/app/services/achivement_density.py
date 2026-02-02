import re

ACTION_VERBS = [
    "increased", "decreased", "reduced", "improved", "optimized",
    "built", "developed", "designed", "led", "scaled", "boosted",
    "enhanced", "automated", "implemented"
]

NUMBER_PATTERN = r"\b\d+(\.\d+)?\s?(%|x|\\+|k|ms|seconds|users|USD|INR)?\b"


def calculate_adi(resume_text: str) -> dict:
    lines = [line.strip() for line in resume_text.split("\n") if line.strip()]
    total_lines = len(lines)

    if total_lines == 0:
        return {
            "adi_score": 0,
            "achievement_count": 0,
            "remarks": "Empty resume"
        }

    achievement_lines = []

    for line in lines:
        has_number = re.search(NUMBER_PATTERN, line, re.I)
        has_action = any(verb in line.lower() for verb in ACTION_VERBS)

        if has_number and has_action:
            achievement_lines.append(line)

    achievement_count = len(achievement_lines)
    raw_adi = achievement_count / total_lines

    # Normalize to 0–10
    adi_score = min(round(raw_adi * 50, 1), 10)

    return {
        "adi_score": adi_score,
        "achievement_count": achievement_count,
        "total_lines": total_lines,
        "sample_achievements": achievement_lines[:3]
    }
