from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserSearchQuery(Base):
    __tablename__ = "user_search_queries"

    id = Column(Integer, primary_key=True, index=True)
    search_question = Column(String, nullable=False)
    user_email = Column(String(255), nullable=False, index=True)
    user_location = Column(String(255))
    user_nationality = Column(String(255))
    thread_id = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    answers = relationship("Answer", back_populates="query")
