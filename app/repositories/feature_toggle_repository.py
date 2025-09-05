from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.feature_toggle_model import FeatureToggle


class FeatureToggleRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(FeatureToggle).all()

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(FeatureToggle).filter(FeatureToggle.name == name).first()

    @staticmethod
    def create(db: Session, feature: FeatureToggle):
        db.add(feature)
        db.commit()
        db.refresh(feature)
        return feature

    @staticmethod
    def update(db: Session, feature: FeatureToggle):
        db.commit()
        db.refresh(feature)
        return feature

    @staticmethod
    def delete(db: Session, feature: FeatureToggle):
        db.delete(feature)
        db.commit()