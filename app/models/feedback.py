from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String, nullable=False)
    details = Column(String, nullable=False)
    file_url = Column(String, nullable=True)
    feedback_reply = Column(Boolean, default=False, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    user_email = Column(String, nullable=False)

    user = relationship("User", backref="feedbacks", foreign_keys=[user_id])
