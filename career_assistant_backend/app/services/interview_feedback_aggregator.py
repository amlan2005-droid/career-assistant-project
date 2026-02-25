from collections import defaultdict

class InterviewFeedbackAggregator:
    def __init__(self):
        self.skill_scores = defaultdict(list)
        self.strengths = set()
        self.weaknesses = set()
        self.improvements = set()
        self.confidence_trend = []
        self.total_questions = 0

    def add_feedback(self, skill, evaluation):
        score = evaluation.get("score", 0)
        confidence = evaluation.get("confidence", 0.5)
        # Use the skill from evaluation if provided, otherwise fallback to session domain
        eval_skill = evaluation.get("skill", skill)

        self.skill_scores[eval_skill].append(score / 10.0) # Normalize to 0-1 as per user example
        self.confidence_trend.append(confidence)
        self.total_questions += 1

        if score >= 7:
            self.strengths.add(f"Strong understanding of {eval_skill}")
        elif score <= 4:
            self.weaknesses.add(f"Weak conceptual clarity in {eval_skill}")
            self.improvements.add(f"Revise fundamentals of {eval_skill}")

    def generate_summary(self):
        avg_scores = {
            skill: sum(scores) / len(scores)
            for skill, scores in self.skill_scores.items()
        }
        
        total_score_sum = sum(sum(scores) for scores in self.skill_scores.values())
        total_count = sum(len(scores) for scores in self.skill_scores.values())
        average_score = total_score_sum / total_count if total_count > 0 else 0

        return {
            "questions_asked": self.total_questions,
            "average_score": round(average_score, 2),
            "skill_scores": dict(self.skill_scores),
            "confidence_trend": self.confidence_trend,
            "strengths": list(self.strengths),
            "weaknesses": list(self.weaknesses),
            "key_improvements": list(self.improvements)
        }
