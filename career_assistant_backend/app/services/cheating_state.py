from enum import Enum

class CheatingSeverity(str, Enum):
    WARNING = "warning"
    TERMINATE = "terminate"

class CheatingEventType(str, Enum):
    TAB_SWITCH = "tab_switch"
    FACE_MISSING = "face_missing"
    MULTIPLE_FACES = "multiple_faces"
    EXTERNAL_DEVICE = "external_device"
