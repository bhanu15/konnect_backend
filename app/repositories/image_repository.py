from sqlalchemy.orm import Session
from app.models.image_model import Image

class ImageRepository:
    @staticmethod
    def create(db: Session, **kwargs) -> Image:
        img = Image(**kwargs)
        db.add(img)
        db.commit()
        db.refresh(img)
        return img

    @staticmethod
    def get(db: Session, image_id: int):
        return db.get(Image, image_id)

    @staticmethod
    def get_by_stored_filename(db: Session, stored_filename: str):
        return db.query(Image).filter(Image.stored_filename == stored_filename).first()

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Image).offset(skip).limit(limit).all()

    @staticmethod
    def delete(db: Session, db_obj: Image):
        db.delete(db_obj)
        db.commit()
        
    @staticmethod
    def get_by_filename(db, filename: str):
        return db.query(Image).filter(Image.filename == filename).first()
