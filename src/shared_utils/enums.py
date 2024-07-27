from enum import Enum, auto


class ThreadState(Enum):
    AWAITING_LOGS = auto()
    LOGS_RECEIVED = auto()
    NO_OLYMPUS_LOGS = auto()
    DCS_LOG_RECEIVED_USER_NO_OLYMPUS_LOG = auto()
    AWAITING_DCS_LOG = auto()
    AWAITING_OLYMPUS_LOG = auto()
    CLOSED = auto()