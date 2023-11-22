from pydantic import BaseModel

from src.common.models import UploadStatus


class HistoryEntity(BaseModel):
    id: int
    status: UploadStatus
    filename: str
    

HistoryResponseModel = list[HistoryEntity]