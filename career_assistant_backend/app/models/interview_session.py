from sqlalchemy import Column, String, Integer, JSON
from app.database.db import Base
from app.services.interview_feedback_aggregator import InterviewFeedbackAggregator

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    domain = Column(String)
    difficulty = Column(String)
    total_questions = Column(Integer, default=5)
    questions = Column(JSON)  # List of questions
    answers = Column(JSON, default=list)
    scores = Column(JSON, default=list)
    confidences = Column(JSON, default=list)
    current_index = Column(Integer, default=0)
    
    # Store feedback summary after interview finishes
    feedback_summary = Column(JSON, nullable=True)
    @property
    def feedback_aggregator(self):
        if not hasattr(self, "_aggregator") or self._aggregator is None:
            self._aggregator = InterviewFeedbackAggregator()
            
            import json
            def ensure_list(val):
                if isinstance(val, str):
                    try: return json.loads(val)
                    except: return []
                return val if isinstance(val, list) else []

            scores = ensure_list(self.scores)
            confidences = ensure_list(self.confidences)
            
            with open("debug_aggregator.log", "a") as f:
                f.write(f"REBUILD for {self.id}: domain={self.domain}, scores={scores}, conf={confidences}\n")

            # Rebuild state from persisted data
            if scores:
                for score in scores:
                    self._aggregator.skill_scores[self.domain].append(score / 10.0)
            
            if confidences:
                self._aggregator.confidence_trend = list(confidences)
                self._aggregator.total_questions = len(confidences)
                    
        return self._aggregator

    def is_completed(self) -> bool:
        return self.current_index >= self.total_questions if self.total_questions else False
