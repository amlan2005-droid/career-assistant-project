from datetime import datetime, timezone
from typing import Dict, List, TypedDict, Optional
from enum import Enum


class RuleType(Enum):
    TAB_SWITCH = "TAB_SWITCH"
    FACE_MISSING = "FACE_MISSING"
    MULTIPLE_FACES = "MULTIPLE_FACES"
    GAZE_OFF_SCREEN = "GAZE_OFF_SCREEN"
    ABNORMAL_HEAD_MOVEMENT = "ABNORMAL_HEAD_MOVEMENT"


class SeverityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CheatingStatus(Enum):
    CLEAN = "clean"
    SUSPICIOUS = "suspicious"
    HIGHLY_SUSPICIOUS = "highly_suspicious"


class Violation(TypedDict):
    rule: str
    severity: str
    score: int
    message: str
    timestamp: str


class CheatingRulesEngine:
    # Thresholds
    SUSPICIOUS_THRESHOLD = 4
    HIGHLY_SUSPICIOUS_THRESHOLD = 8

    def __init__(self):
        self.violations: List[Violation] = []
        self.warning_count = 0
        self.cheating_score = 0  # aggregate score

    # ---------------- TAB SWITCH ----------------
    def tab_switch_detected(self):
        self._add_violation(
            rule=RuleType.TAB_SWITCH,
            severity=SeverityLevel.MEDIUM,
            score=2,
            message="User switched browser tab during interview."
        )

    # ---------------- FACE NOT DETECTED ----------------
    def face_missing(self, seconds_missing: float):
        if seconds_missing >= 5:
            self._add_violation(
                rule=RuleType.FACE_MISSING,
                severity=SeverityLevel.HIGH,
                score=3,
                message=f"Face not detected for {seconds_missing:.1f} seconds."
            )

    # ---------------- MULTIPLE FACES ----------------
    def multiple_faces_detected(self, face_count: int):
        if face_count > 1:
            self._add_violation(
                rule=RuleType.MULTIPLE_FACES,
                severity=SeverityLevel.CRITICAL,
                score=5,
                message=f"{face_count} faces detected in frame."
            )

    # ---------------- GAZE OFF SCREEN ----------------
    def gaze_off_screen(self, duration: float):
        if duration >= 3:
            self._add_violation(
                rule=RuleType.GAZE_OFF_SCREEN,
                severity=SeverityLevel.MEDIUM,
                score=2,
                message=f"User looked away from screen for {duration:.1f} seconds."
            )

    # ---------------- HEAD MOVEMENT ----------------
    def abnormal_head_movement(self):
        self._add_violation(
            rule=RuleType.ABNORMAL_HEAD_MOVEMENT,
            severity=SeverityLevel.LOW,
            score=1,
            message="Suspicious head movement detected."
        )

    # ---------------- INTERNAL HELPER ----------------
    def _add_violation(self, rule: RuleType, severity: SeverityLevel, score: int, message: str):
        violation: Violation = {
            "rule": rule.value,
            "severity": severity.value,
            "score": score,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        self.violations.append(violation)
        self.cheating_score += score
        
        # Increase warning count for significant violations
        if severity in [SeverityLevel.MEDIUM, SeverityLevel.HIGH, SeverityLevel.CRITICAL]:
            self.warning_count += 1

    # ---------------- SUMMARY ----------------
    def summary(self) -> Dict:
        status = CheatingStatus.CLEAN

        if self.cheating_score >= self.HIGHLY_SUSPICIOUS_THRESHOLD:
            status = CheatingStatus.HIGHLY_SUSPICIOUS
        elif self.cheating_score >= self.SUSPICIOUS_THRESHOLD:
            status = CheatingStatus.SUSPICIOUS

        return {
            "status": status.value,
            "cheating_score": self.cheating_score,
            "warning_count": self.warning_count,
            "violations": self.violations
        }

    # ---------------- RESET SESSION ----------------
    def reset(self):
        self.violations.clear()
        self.cheating_score = 0
        self.warning_count = 0


# Session-based tracking
CHEATING_SESSIONS: Dict[str, Dict] = {}
MAX_WARNINGS = 5
TERMINATION_EVENTS = {
    "multiple_faces",
    "external_device"
}


def process_cheating_event(session_id: str, event_type: str):
    session = CHEATING_SESSIONS.setdefault(session_id, {
        "warnings": 0,
        "terminated": False,
        "auto_submitted": False,
        "events": [],
        "engine": CheatingRulesEngine()
    })

    session["events"].append(event_type)

    # 🚨 Hard violations
    if event_type in TERMINATION_EVENTS:
        session["terminated"] = True
        return {
            "action": "TERMINATE",
            "reason": event_type
        }

    # ⚠️ Soft violations
    session["warnings"] += 1

    if session["warnings"] >= MAX_WARNINGS:
        session["auto_submitted"] = True
        return {
            "action": "AUTO_SUBMIT",
            "warnings": session["warnings"]
        }

    return {
        "action": "WARNING",
        "warnings": session["warnings"]
    }
