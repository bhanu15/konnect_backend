import os
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.repositories.image_crud import image_crud
from app.schemas.image_schema import ImageUpdate
from app.models.image_model import Image

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ImageService:
    def upload_image(self, db: Session, file: UploadFile, description: str | None):
        if not file.filename:
            raise ValueError("Uploaded file must have a filename")
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        return image_crud.create(db, filename=file.filename, path=file_path, description=description)

    def get_image(self, db: Session, image_id: int) -> Image | None:
        return image_crud.get(db, image_id)

    def list_images(self, db: Session, skip: int = 0, limit: int = 10):
        return image_crud.list(db, skip, limit)

    def update_image(self, db: Session, image_id: int, update_data: ImageUpdate):
        db_obj = image_crud.get(db, image_id)
        if not db_obj:
            return None
        return image_crud.update(db, db_obj, update_data)

    def delete_image(self, db: Session, image_id: int):
        db_obj = image_crud.get(db, image_id)
        if not db_obj:
            return None
        image_crud.delete(db, db_obj)
        return db_obj

image_service = ImageService()
