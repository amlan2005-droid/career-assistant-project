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
- DO NOT default to 6. Use the full 0-10 range based on the rules above.
- Be critical. If an answer is just a textbook definition without application, it is 5-6 at best.

Question: {question}
Answer: {answer}
Difficulty: {difficulty}

Evaluation style:
{style}

Return ONLY a JSON object with:
- score: integer (0-10)
- strength: short string
- weakness: short string
- feedback: concise improvement suggestion
"""

    response_text = ask_gemini(prompt)
    
    try:
        # 1. Try to find content within triple backticks first
        code_block_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL | re.IGNORECASE)
        if code_block_match:
            return json.loads(code_block_match.group(1))

        # 2. Try to find the first '{' and last '}'
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
            
        print(f"FAILED TO PARSE JSON. RAW RESPONSE: {response_text}")
        return {"score": 2, "strength": "N/A", "weakness": "Evaluation failed", "feedback": "AI failed to parse response format."}
    except Exception as e:
        print(f"EVALUATION ERROR: {e}. RAW: {response_text}")
        return {"score": 2, "strength": "N/A", "weakness": "Evaluation failed", "feedback": "AI response processing error."}


def finalize_interview(session_id: str) -> dict:
    """
    Mock implementation of finalize_interview.
    """
    return {
        "final_score": 80,
        "feedback": "Good job! You demonstrated solid understanding."
    }
