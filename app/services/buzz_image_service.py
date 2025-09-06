import boto3
import uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.core.config import settings
from app.repositories.buzz_image_repository import BuzzImageRepository

class BuzzImageService:
    s3_client = boto3.client(
        "s3",
        region_name=settings.S3_REGION,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY
    )

    @staticmethod
    def save_image(db: Session, file: UploadFile, title: str, description: str | None = None):
        if file.content_type not in settings.ALLOWED_CONTENT_TYPES:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        file.file.seek(0, 2)  # Move to end of file
        file_size = file.file.tell()
        file.file.seek(0)  # Reset pointer to start
        if file_size > settings.MAX_UPLOAD_SIZE_BYTES:
            raise HTTPException(status_code=413, detail="File too large")

        # generate unique key
        if not file.filename:
            raise HTTPException(status_code=400, detail="File must have a filename")
        ext = file.filename.split(".")[-1]
        key = f"{uuid.uuid4().hex}_{title.replace(' ', '-')}.{ext}"

        try:
            BuzzImageService.s3_client.upload_fileobj(
                file.file,
                settings.S3_BUCKET,
                key,
                ExtraArgs={"ContentType": file.content_type}  # no ACL
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"S3 upload failed: {e}")

        public_url = f"https://{settings.S3_BUCKET}.s3.{settings.S3_REGION}.amazonaws.com/{key}"

        return BuzzImageRepository.create(
            db=db,
            title=title,
            description=description,
            url=public_url
        )

    @staticmethod
    def get_image_by_id(db: Session, image_id: int):
        img = BuzzImageRepository.get(db, image_id)
        if not img or img.is_deleted.is_(True):
            raise HTTPException(status_code=404, detail="Image not found")
        return img

    @staticmethod
    def list_images(db: Session, skip=0, limit=100):
        return BuzzImageRepository.list(db, skip, limit)

    @staticmethod
    def update_image(db: Session, image_id: int, title: str | None = None, description: str | None = None):
        img = BuzzImageRepository.get(db, image_id)
        if not img or img.is_deleted.is_(True):
            raise HTTPException(status_code=404, detail="Image not found")
        return BuzzImageRepository.update(
            db,
            img,
            title=title if title is not None else getattr(img, "title"),
            description=description if description is not None else getattr(img, "description")
        )

    @staticmethod
    def delete_image(db: Session, image_id: int):
        img = BuzzImageRepository.get(db, image_id)
        if not img or img.is_deleted.is_(True):
            raise HTTPException(status_code=404, detail="Image not found")
        return BuzzImageRepository.soft_delete(db, img)
