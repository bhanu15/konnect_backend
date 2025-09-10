from sqlalchemy import Column, String, Boolean, Integer
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sub = Column(String, unique=True, index=True)   # Google unique ID
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    given_name = Column(String)
    family_name = Column(String)
    picture = Column(String)  # stored as plain string
    email_verified = Column(Boolean, default=False)

    # ✅ New fields
    is_admin = Column(Boolean, default=False)   # admin flag
    is_active = Column(Boolean, default=True)   # active status

    is_deleted = Column(Boolean, default=False)  # soft delete
