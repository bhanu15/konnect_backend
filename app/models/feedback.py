from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(100), nullable=False)
    details = Column(String, nullable=False)
    file_url = Column(String, nullable=True)
    feedback_reply = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    user_email = Column(String(100), nullable=False)
