from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional

class FeedbackBase(BaseModel):
    type: str
    details: str
    file_url: Optional[HttpUrl] = None
    feedback_reply: Optional[bool] = False
    is_deleted: Optional[bool] = False
    user_id: Optional[int] = None
    user_email: EmailStr

    class Config:
        orm_mode = True
        json_encoders = {HttpUrl: str}

class FeedbackCreate(BaseModel):
    type: str
    details: str
    user_email: EmailStr
    user_id: Optional[int] = None

class FeedbackUpdate(BaseModel):
    type: Optional[str] = None
    details: Optional[str] = None

class FeedbackResponse(FeedbackBase):
    id: int
