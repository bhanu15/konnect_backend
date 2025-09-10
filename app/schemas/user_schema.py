from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[HttpUrl] = None
    email_verified: Optional[bool] = False

    class Config:
        orm_mode = True
        json_encoders = {HttpUrl: str}

class UserCreate(UserBase):
    sub: str
    # is_admin, is_active are intentionally excluded (can only be set later)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[HttpUrl] = None
    email_verified: Optional[bool] = None
    is_active: Optional[bool] = None   # allow toggling active status
    is_admin: Optional[bool] = None    # only if authorized

    class Config:
        orm_mode = True
        json_encoders = {HttpUrl: str}

class UserResponse(UserBase):
    user_id: int
    sub: str
    is_deleted: bool
    is_admin: bool
    is_active: bool

    class Config:
        orm_mode = True
        json_encoders = {HttpUrl: str}
