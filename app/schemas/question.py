from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --------- Request Schemas ---------
class QuestionCreate(BaseModel):
    question_text: str
    asked_by: str

class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    answer: Optional[str] = None
    # 🚫 answered_by / answered_at controlled by service only

# --------- Response Schema ---------
class QuestionResponse(BaseModel):
    id: int
    question_text: str
    asked_by: str
    asked_at: datetime
    answer: Optional[str]
    answered_by: Optional[str]
    answered_at: Optional[datetime]

    class Config:
        orm_mode = True
