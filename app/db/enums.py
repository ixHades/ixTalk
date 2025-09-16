from enum import Enum


class MessageStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECT = "reject"


class WarningSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AdminRole(str, Enum):
    SUPER = "super"
    REVIEWER = "reviewer"


class LogLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
