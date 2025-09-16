from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSearchQueryCreate(BaseModel):
    searchQuestion: str
    userEmail: EmailStr
    userLocation: Optional[str]
    userNationality: Optional[str]

class UserSearchQueryResponse(BaseModel):
    searchQuestion: str
    userEmail: EmailStr
    userLocation: Optional[str]
    userNationality: Optional[str]
    threadId: Optional[str]

    class Config:
        orm_mode = True
