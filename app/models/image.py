from sqlalchemy import Column, Integer, String, DateTime,Text, func
from app.db.session import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    description = Column(String, nullable=True)
    path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    url = Column(Text, nullable=False)          # public URL
    content_type = Column(String(100))
    size_bytes = Column(Integer)
