from pydantic import BaseModel

from src.common.models import UploadStatus


class HistoryEntity(BaseModel):
    id: int
    index: int
    status: UploadStatus
    filename: str
    

HistoryResponseModel = list[HistoryEntity]


class ResultEntity(BaseModel):
    id: int
    name: str
    src: str
    year: int
    title: str
    affiliation: str
    
    
SuggestionsResponseModel = list[ResultEntity]
