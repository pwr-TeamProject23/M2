from enum import Enum


class SearchTaskStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    ERROR = "error"
