from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class ExpertQuestion(Base):
    __tablename__ = "expert_question"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    asked_by = Column(String, nullable=False)
    asked_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    answer = Column(Text, nullable=True)
    answered_by = Column(String, nullable=True)
    answered_at = Column(DateTime(timezone=True), nullable=True)
