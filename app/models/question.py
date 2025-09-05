from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.db.base import Base

class ExpertQuestion(Base):
    __tablename__ = "expert_question"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(255), nullable=False, index=True)
    question = Column(String(255), nullable=False)
    answer = Column(Text, nullable=True)
    answered_by_email = Column(String(255), nullable=True, index=True)
    asked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    answered_at = Column(DateTime, nullable=True)
