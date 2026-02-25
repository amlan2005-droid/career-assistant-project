from collections import defaultdict
import logging
import random
import re
import uuid
from app.services.gemini_client import ask_gemini


logger = logging.getLogger(__name__)

MAX_QUESTIONS = 15


class InterviewState:
    def __init__(self):
        self.questions_asked = 0
        self.scores = []
        self.skill_scores = defaultdict(list)
        self.confidence_trend = []

    def update(self, score: float, skill: str, confidence: float):
        self.questions_asked += 1
        self.scores.append(score)
        self.skill_scores[skill].append(score)
        self.confidence_trend.append(confidence)

    @property
    def average_score(self):
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)

    def to_dict(self):
        return {
            "questions_asked": self.questions_asked,
            "average_score": round(self.average_score, 2),
            "skill_scores": dict(self.skill_scores),
            "confidence_trend": self.confidence_trend,
        }


INTERVIEW_SESSIONS: dict[str, InterviewState] = {}


def extract_skills(resume_profile):
    if not resume_profile:
        return []
    if isinstance(resume_profile, dict):
        return resume_profile.get("skills", [])
    return getattr(resume_profile, "skills", [])


def sanitize_question(text: str) -> str:
    text = text.strip()
    text = re.sub(r'^[\d\.\)\-]+\s*', '', text)
    text = text.split('\n')[0]
    return text[:400]


def estimate_confidence(answer: str) -> float:
    length_score = min(len(answer.split()) / 120, 1.0)
    filler_penalty = len(
        re.findall(r'\b(uh|um|maybe|not sure)\b', answer.lower())
    ) * 0.05
    return max(0.1, min(1.0, length_score - filler_penalty))


LOGICAL_SCENARIO_BANK = {
    "python-backend": [
        "A Python production service is experiencing an intermittent memory leak that only appears on Fridays. Walk me through your logical steps to isolate the bottleneck.",
        "You need to process 10GB of CSV data on a machine with only 2GB of RAM. How would you design the data pipeline logically using Python?",
        "If you discover a race condition in your asynchronous Python service, how would you logically diagnose which shared resource is causing the conflict?",
        "Your Python API is slow. You've narrowed it down to either the database query or the serialization layer. How do you logically prove which one is the culprit?",
        "Imagine you're building a real-time notification system. Would you choose multi-threading or asyncio? Explain the logical trade-offs for this scenario."
    ],
    "java-backend": [
        "Your Java application is throwing 'OutOfMemoryError', but the heap dump shows plenty of space. What logical paths would you investigate next?",
        "Design a logical thread-safe mechanism for a shared counter in a high-concurrency Java environment without using 'synchronized'.",
        "A legacy Java service is slow. You suspect a database connection leak. How would you logically verify this and trace the leak to its source?",
        "If you had to choose between Microservices and a Monolith for a new Java start-up project, what logical criteria would you use to decide?",
        "Your application is hanging in production. Walk me through the logical steps of analyzing a thread dump to find the deadlock."
    ],
    "react-frontend": [
        "A React component is re-rendering 50 times per second. How would you logically trace exactly which state or prop change is triggering the excess renders?",
        "You're building a dashboard that handles thousands of live data points. What logical strategy would you use to keep the UI responsive?",
        "A user reports that the app state is inconsistent after navigating back and forth. How would you logically debug the state synchronization issue?",
        "If you were tasked with migrating a large React app to Next.js, what logical steps would you take to ensure no regressions in user experience?",
        "You have a memory leak in a React app that occurs only after 10 minutes of usage. How would you logically use browser dev tools to find it?"
    ],
    "devops": [
        "A CI/CD pipeline failed but only in the 'Production' environment. It works in 'Staging'. What logical discrepancies would you investigate first?",
        "Your Kubernetes Pod is stuck in 'CrashLoopBackOff'. Walk me through your logical sequence of commands to find the root cause.",
        "A database migration took down your service. How would you logically design a rollback strategy that ensures no data is lost?",
        "You're seeing a spike in 5xx errors on your load balancer. How do you logically determine if the issue is the network, the LB, or the upstream services?",
        "Design a logical backup and recovery plan for a stateful set in Kubernetes. What are the critical failure points you'd consider?"
    ],
    "general": [
        "You're given a bug report with no clear reproduction steps. What is your logical framework for narrowing down the possible causes?",
        "Two services need to communicate. One is much faster than the other. What logical patterns (queues, retries, etc.) would you use to bridge the gap?",
        "If you had to optimize a system for 'Cost' vs 'Latency', what logical compromises would you make in each scenario?",
        "You discover a security vulnerability in a third-party library. How do you logically assess and mitigate the risk without breaking the app?",
        "A system you didn't build is crashing intermittently. How do you logically approach learning the architecture while trying to fix the bug?"
    ]
}


def generate_resume_aware_questions(
    domain: str,
    resume_profile,
    difficulty: str = "medium",
    question_count: int = 5,
    previous_questions: list[str] | None = None
) -> list[str]:

    if previous_questions is None:
        previous_questions = []

    DIFFICULTY_RULES = {
        "easy": {
            "style": "Simple logical puzzles, basic troubleshooting, and high-level workflows.",
            "complexity": "Ask the candidate to explain the 'Logic' behind a simple task or fix."
        },
        "medium": {
            "style": "Complex situational scenarios involving trade-offs, debugging, and architectural logic.",
            "complexity": "Present a realistic problem 'Scenario' where they must walk through their logical reasoning steps."
        },
        "hard": {
            "style": "Deep system-level puzzles, critical failure modes, and optimization trade-offs.",
            "complexity": "Challenge their logical consistency under pressure and with constraints."
        }
    }

    diff_settings = DIFFICULTY_RULES.get(difficulty, DIFFICULTY_RULES["medium"])
    resume_skills = extract_skills(resume_profile)

    seed = random.randint(1, 1_000_000)
    previous_q_text = "\n- ".join(previous_questions) if previous_questions else "None"

    prompt = f"""
You are an expert technical interviewer who focuses on LOGICAL THINKING and PROBLEM-SOLVING SCENARIOS.

Domain: {domain}
Difficulty: {difficulty}
Candidate Skills: {', '.join(resume_skills) if resume_skills else 'General skills'}

RULES:
1. Generate exactly {question_count} questions.
2. Every question MUST be a 'Scenario' or 'Situational Puzzle' that requires logical reasoning.
3. No labels or headers.
4. Output ONLY a numbered list.
5. Pattern:
   - Provide a realistic context or problem.
   - Ask for the candidate's logical approach or solution.
   - {diff_settings['style']}
   - {diff_settings['complexity']}
6. Avoid repeating:
   - {previous_q_text}
7. Seed: {seed}

Generate logical scenarios:
"""

    response = ask_gemini(prompt)

    if response.startswith("ERROR:"):
        logger.warning(f"AI Scenario generation failed, falling back to bank: {response}")
        # High-quality fallback from bank
        bank_questions = LOGICAL_SCENARIO_BANK.get(domain, LOGICAL_SCENARIO_BANK["general"])
        # Filter out previously asked questions if any
        available = [q for q in bank_questions if q not in previous_questions]
        if not available: available = bank_questions
        
        fallback = random.sample(available, min(len(available), question_count))
        # If we still need more, add a logical variant
        while len(fallback) < question_count:
            fallback.append(f"Scenario: You've discovered a bottleneck in your {domain} integration. Walk me through your logical steps to debug it.")
        return fallback

    matches = re.findall(r'^\d+[\.\)]\s*(.*)', response, re.MULTILINE)
    questions = matches if matches else [
        re.sub(r'^\d+[\.\)]\s*', '', l)
        for l in response.split('\n') if l.strip()
    ]

    questions = [q for q in questions if len(q) > 15]
    
    # Final safety check: if AI returned trash, use bank
    if not questions:
        bank_questions = CONCEPTUAL_QUESTION_BANK.get(domain, CONCEPTUAL_QUESTION_BANK["general"])
        return random.sample(bank_questions, min(len(bank_questions), question_count))

    return questions[:question_count]


def start_interview(domain: str, resume_profile):
    session_id = str(uuid.uuid4())
    state = InterviewState()
    INTERVIEW_SESSIONS[session_id] = state

    questions = generate_resume_aware_questions(
        domain=domain,
        resume_profile=resume_profile,
        difficulty="medium"
    )

    return {
        "session_id": session_id,
        "questions": questions,
        "state": state.to_dict()
    }


def submit_answer(
    session_id: str,
    answer: str,
    skill: str,
    score: float
):
    state = INTERVIEW_SESSIONS.get(session_id)
    if not state:
        raise ValueError("Invalid interview session")

    confidence = estimate_confidence(answer)
    state.update(score=score, skill=skill, confidence=confidence)

    next_question = generate_next_adaptive_question(
        domain=skill,
        difficulty="medium",
        state_summary=state.to_dict(),
        previous_questions=[]
    )

    return {
        "next_question": next_question,
        "state": state.to_dict(),
        "interview_complete": next_question is None
    }


def generate_next_adaptive_question(
    domain: str,
    difficulty: str,
    state_summary: dict,
    previous_questions: list[str]
) -> str | None:

    questions_asked = state_summary.get("questions_asked", 0)

    if questions_asked >= MAX_QUESTIONS:
        return None

    avg_score = state_summary.get("average_score", 0.5)
    skill_scores = state_summary.get("skill_scores", {})
    confidence_trend = state_summary.get("confidence_trend", [])

    recent_confidence = confidence_trend[-1] if confidence_trend else 0.5

    weak_skills = [
        s for s, scores in skill_scores.items()
        if sum(scores) / len(scores) < 0.5
    ]
    strong_skills = [
        s for s, scores in skill_scores.items()
        if sum(scores) / len(scores) > 0.8
    ]

    prompt = f"""
You are an adaptive technical interviewer focusing on LOGICAL REASONING.

Domain: {domain}
Difficulty: {difficulty}
Questions Asked: {questions_asked}
Average Score: {avg_score}
Confidence: {recent_confidence}
Weak Skills: {', '.join(weak_skills) or 'None'}
Strong Skills: {', '.join(strong_skills) or 'None'}

Avoid repeating:
{chr(10).join(f"- {q}" for q in previous_questions)}

Generate exactly ONE follow-up SITUATIONAL or LOGICAL question.
- It must be a scenario where the candidate has to troubleshoot, decide between trade-offs, or explain a complex workflow.
- Your goal is to see how they reason through an unexpected problem.
"""

    response = ask_gemini(prompt)
    if response.startswith("ERROR:"):
        logger.warning(f"AI Adaptive scenario failed, falling back to bank: {response}")
        bank_questions = LOGICAL_SCENARIO_BANK.get(domain, LOGICAL_SCENARIO_BANK["general"])
        available = [q for q in bank_questions if q not in previous_questions]
        if not available: available = bank_questions
        return random.choice(available)

    return sanitize_question(response)
