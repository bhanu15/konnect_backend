from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base


class FeatureToggle(Base):
	__tablename__ = "feature_toggles"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String(100), unique=True, nullable=False, index=True)
	description = Column(String(255), nullable=True)
	is_enabled = Column(Boolean, default=False, nullable=False)