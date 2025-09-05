from sqlalchemy.orm import Session
from app.models.image_model import Image
from app.schemas.image_schema import ImageUpdate

class ImageCRUD:
    def create(self, db: Session, filename: str, path: str, description: str | None):
        db_obj = Image(filename=filename, path=path, description=description)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, image_id: int):
        return db.query(Image).filter(Image.id == image_id).first()

    def list(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(Image).offset(skip).limit(limit).all()

    def update(self, db: Session, db_obj: Image, update_data: ImageUpdate):
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Image):
        db.delete(db_obj)
        db.commit()

image_crud = ImageCRUD()
