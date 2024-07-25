from enum import Enum, auto


class ThreadState(Enum):
    AWAITING_LOGS = auto()
    LOGS_RECEIVED = auto()
    NO_OLYMPUS_LOGS = auto()
    DCS_LOG_RECEIVED = auto()
    CLOSED = auto()