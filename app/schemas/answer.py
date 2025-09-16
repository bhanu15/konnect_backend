from pydantic import BaseModel
from datetime import datetime

class AnswerResponse(BaseModel):
    id: int
    queryId: int
    answerText: str
    createdAt: datetime

    class Config:
        orm_mode = True
