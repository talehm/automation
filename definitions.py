from enum import Enum


class ExecutionStatus(Enum):
    LIMIT_EXCEEDED = "LIMIT_EXCEEDED"
    FAILED = "FAILED"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    SUCCESS = "SUCCESS"
