from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional

class FeedbackBase(BaseModel):
    type: str
    details: str
    file_url: Optional[HttpUrl] = None
    feedback_reply: Optional[bool] = False
    is_deleted: Optional[bool] = False
    user_email: EmailStr

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackUpdate(BaseModel):
    type: Optional[str] = None
    details: Optional[str] = None
    file_url: Optional[HttpUrl] = None
    feedback_reply: Optional[bool] = None

class FeedbackResponse(FeedbackBase):
    id: int

    class Config:
        orm_mode = True
