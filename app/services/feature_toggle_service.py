from sqlalchemy.orm import Session
from app.repositories.feature_toggle_repository import FeatureToggleRepository
from app.models.feature_toggle_model import FeatureToggle
from app.schemas.feature_toggle_schema import FeatureToggleCreate, FeatureToggleUpdate


class FeatureToggleService:

	@staticmethod
	def list_toggles(db: Session):
		return FeatureToggleRepository.get_all(db)

	@staticmethod
	def create_toggle(db: Session, data: FeatureToggleCreate):
		existing = FeatureToggleRepository.get_by_name(db, data.name)
		if existing:
			raise ValueError("Feature with this name already exists")
		feature = FeatureToggle(**data.dict())
		return FeatureToggleRepository.create(db, feature)

	@staticmethod
	def update_toggle(db: Session, name: str, data: FeatureToggleUpdate):
		feature = FeatureToggleRepository.get_by_name(db, name)
		if not feature:
			return None
		for key, value in data.dict(exclude_unset=True).items():
			setattr(feature, key, value)
		return FeatureToggleRepository.update(db, feature)

	@staticmethod
	def delete_toggle(db: Session, name: str):
		feature = FeatureToggleRepository.get_by_name(db, name)
		if not feature:
			return False
		FeatureToggleRepository.delete(db, feature)
		return True

	@staticmethod
	def is_enabled(db: Session, name: str) -> bool:
		feature = FeatureToggleRepository.get_by_name(db, name)
		return bool(feature.is_enabled) if feature else False