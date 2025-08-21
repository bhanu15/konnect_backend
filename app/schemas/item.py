from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    title: str
    description: Optional[str] = None

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ItemRead(BaseModel):
    id: int
    title: str
    description: Optional[str]

    class Config:
        orm_mode = True

