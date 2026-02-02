from collections import defaultdict

class InterviewFeedbackAggregator:
    def __init__(self):
        self.skill_scores = defaultdict(list)
        self.strengths = set()
        self.weaknesses = set()
        self.improvements = set()

    def add_feedback(self, skill, evaluation):
        score = evaluation["score"]

        self.skill_scores[skill].append(score)

        if score >= 7:
            self.strengths.add(
                f"Strong understanding of {skill}"
            )
        elif score <= 4:
            self.weaknesses.add(
                f"Weak conceptual clarity in {skill}"
            )
            self.improvements.add(
                f"Revise fundamentals and real-world use cases of {skill}"
            )

    def generate_summary(self):
        avg_scores = {
            skill: sum(scores) / len(scores)
            for skill, scores in self.skill_scores.items()
        }

        return {
            "strengths": list(self.strengths),
            "weaknesses": list(self.weaknesses),
            "key_improvements": list(self.improvements),
            "skill_wise_scores": avg_scores
        }
