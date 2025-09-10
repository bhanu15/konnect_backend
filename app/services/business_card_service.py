import uuid
import boto3
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.repositories.business_card_repository import BusinessCardRepository
from app.schemas.business_card_schema import BusinessCardCreate
from app.core.config import settings

class BusinessCardService:
    s3_client = boto3.client(
        "s3",
        region_name=settings.S3_REGION,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
    )

    @staticmethod
    def _upload_to_s3(file: UploadFile) -> str:
        try:
            bucket_name = settings.S3_BUCKET
            key = f"business_cards/{uuid.uuid4()}-{file.filename}"
            BusinessCardService.s3_client.upload_fileobj(
                file.file,
                bucket_name,
                key,
                ExtraArgs={"ContentType": file.content_type},
            )
            return f"https://{bucket_name}.s3.{settings.S3_REGION}.amazonaws.com/{key}"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"S3 upload failed: {str(e)}")

    @staticmethod
    def create_card(db: Session, card_data: BusinessCardCreate, file: UploadFile):
        # File is uploaded only after form validation
        file_url = BusinessCardService._upload_to_s3(file)
        return BusinessCardRepository.create(db, card_data, file_url)

    @staticmethod
    def get_card(db: Session, card_id: int):
        card = BusinessCardRepository.get_by_id(db, card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Business card not found")
        return card

    @staticmethod
    def list_cards(db: Session, skip: int = 0, limit: int = 100):
        return BusinessCardRepository.list(db, skip, limit)

    @staticmethod
    def delete_card(db: Session, card_id: int):
        card = BusinessCardRepository.soft_delete(db, card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Business card not found")
        return {"detail": "Business card deleted successfully"}

    @staticmethod
    def search_cards(db: Session, email: str | None = None, phone_number: str | None = None,
                     skip: int = 0, limit: int = 100, sort_by: str = "company_name", sort_order: str = "asc"):
        return BusinessCardRepository.search(db, email=email, phone_number=phone_number,
                                             skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order)
