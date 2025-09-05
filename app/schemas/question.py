from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class QuestionBase(BaseModel):
    user_email: str
    question: str
    answer: Optional[str] = None
    answered_by_email: Optional[str] = None
    asked_at: Optional[datetime] = None
    answered_at: Optional[datetime] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: int
    class Config:
        orm_mode = True
