from pydantic import BaseModel
from datetime import datetime


class BuzzImageBase(BaseModel):
    title: str
    description: str | None = None


class BuzzImageCreate(BuzzImageBase):
    pass


class BuzzImageUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class BuzzImageOut(BuzzImageBase):
    id: int
    url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
