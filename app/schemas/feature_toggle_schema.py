from pydantic import BaseModel
from typing import Optional


class FeatureToggleBase(BaseModel):
	name: str
	description: Optional[str] = None
	is_enabled: bool = False


class FeatureToggleCreate(FeatureToggleBase):
	pass


class FeatureToggleUpdate(BaseModel):
	description: Optional[str] = None
	is_enabled: Optional[bool] = None


class FeatureToggleOut(FeatureToggleBase):
	id: int


class Config:
	orm_mode = True