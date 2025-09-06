from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from app.db.base import Base


class BuzzImage(Base):
    __tablename__ = "buzz_images"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    url = Column(String, nullable=False)  # S3 URL
    is_deleted = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
