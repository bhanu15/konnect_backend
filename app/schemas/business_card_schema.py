from pydantic import BaseModel, HttpUrl, EmailStr, validator, ValidationError
from typing import Optional
import re

class BusinessCardBase(BaseModel):
    company_name: str
    phone_number: str
    email: EmailStr
    file_url: HttpUrl
    is_deleted: Optional[bool] = False

    class Config:
        orm_mode = True
        json_encoders = {HttpUrl: str}

class BusinessCardCreate(BaseModel):
    company_name: str
    phone_number: str
    email: EmailStr

    @validator("phone_number")
    def validate_phone_number(cls, v):
        # Allow only digits, optional + at start, length 7-15
        pattern = re.compile(r"^\+?\d{7,15}$")
        if not pattern.match(v):
            raise ValueError("Invalid phone number format")
        return v

class BusinessCardResponse(BusinessCardBase):
    id: int
