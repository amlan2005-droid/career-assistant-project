from sqlalchemy import Column, String, Integer, JSON
from app.database.db import Base
from app.services.interview_feedback_aggregator import InterviewFeedbackAggregator

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    domain = Column(String)
    difficulty = Column(String)
    questions = Column(JSON)  # List of questions
    answers = Column(JSON, default=list)
    scores = Column(JSON, default=list)
    current_index = Column(Integer, default=0)
    
    # Store feedback summary after interview finishes
    feedback_summary = Column(JSON, nullable=True)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure lists and index are initialized even if not passed in kwargs
        # This is critical for in-memory objects that aren't yet persisted
        if self.answers is None:
            self.answers = []
        if self.scores is None:
            self.scores = []
        if self.current_index is None:
            self.current_index = 0
            
        # Runtime aggregator
        self._aggregator = InterviewFeedbackAggregator()

    @property
    def feedback_aggregator(self):
        if not hasattr(self, "_aggregator") or self._aggregator is None:
            self._aggregator = InterviewFeedbackAggregator()
            # If we already have some answers/scores (e.g. from DB load), we might want to populate it?
            # For now, it's mostly used during a single active session lifetime.
        return self._aggregator

    def is_completed(self) -> bool:
        return self.current_index >= len(self.questions) if self.questions else False
