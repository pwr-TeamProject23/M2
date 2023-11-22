from enum import Enum


class UploadStatus(Enum):
    PENDING = "pending"
    READY = "ready"
    ERROR = "error"
