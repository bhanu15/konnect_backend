from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class BusinessCard(Base):
    __tablename__ = "business_cards"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    company_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)
