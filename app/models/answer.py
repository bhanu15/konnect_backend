from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("user_search_queries.id"))
    answer_text = Column(String, nullable=False)

    query = relationship("UserSearchQuery", back_populates="answers")
