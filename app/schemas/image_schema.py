from pydantic import BaseModel
from datetime import datetime

class ImageBase(BaseModel):
    description: str | None = None

class ImageCreate(ImageBase):
    pass

class ImageUpdate(ImageBase):
    pass

class ImageOut(ImageBase):
    id: int
    filename: str
    path: str
    created_at: datetime

    class Config:
        orm_mode = True
