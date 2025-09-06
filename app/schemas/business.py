from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
import re

class BusinessBase(BaseModel):
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    comment: Optional[str] = None

    @validator("email")
    def validate_email(cls, v):
        if v is None:
            return v
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")
        return v

    @validator("phone")
    def validate_phone(cls, v):
        if v is None:
            return v
        pattern = r"^\+?[0-9\s\-]{7,15}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid phone number format")
        return v

class BusinessCreate(BusinessBase):
    company_name: str
    contact_name: str
    email: EmailStr

class BusinessUpdate(BusinessBase):
    pass

class BusinessResponse(BusinessBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class PaginatedResponse(BaseModel):
    total: int
    skip: int
    limit: int
    results: List[BusinessResponse]
