import uuid
import boto3
from fastapi import UploadFile, HTTPException
from typing import Optional, List
from sqlalchemy.orm import Session

from app.repositories.feedback_repository import FeedbackRepository
from app.schemas.feedback_schema import FeedbackCreate, FeedbackUpdate
from app.models.feedback import Feedback
from app.core.config import settings

class FeedbackService:
    s3_client = boto3.client(
        "s3",
        region_name=settings.S3_REGION,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY
    )

    @staticmethod
    def _upload_to_s3(file: UploadFile) -> str:
        try:
            bucket_name = settings.S3_BUCKET
            key = f"feedback/{uuid.uuid4()}-{file.filename}"
            FeedbackService.s3_client.upload_fileobj(
                file.file,
                settings.S3_BUCKET,
                key,
                ExtraArgs={"ContentType": file.content_type}  # no ACL
            )
            return f"https://{bucket_name}.s3.{settings.S3_REGION}.amazonaws.com/{key}"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"S3 upload failed: {str(e)}")

    @staticmethod
    def create_feedback(db: Session, feedback_data: FeedbackCreate, file: Optional[UploadFile] = None) -> Feedback:
        file_url = FeedbackService._upload_to_s3(file) if file else None
        return FeedbackRepository.create(db, feedback_data, file_url)

    @staticmethod
    def get_feedback_by_id(db: Session, feedback_id: int) -> Feedback:
        feedback = FeedbackRepository.get_by_id(db, feedback_id)
        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback not found")
        return feedback


    @staticmethod
    def update_feedback(db: Session, feedback_id: int, feedback_update: FeedbackUpdate, file: Optional[UploadFile] = None) -> Feedback:
        file_url = FeedbackService._upload_to_s3(file) if file else None
        feedback = FeedbackRepository.update(db, feedback_id, feedback_update, file_url)
        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback not found")
        return feedback 

    @staticmethod
    def delete_feedback(db: Session, feedback_id: int):
        feedback = FeedbackRepository.soft_delete(db, feedback_id)
        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback not found")
        return {"detail": "Feedback deleted successfully"}

    @staticmethod
    def mark_as_replied(db: Session, feedback_id: int) -> Feedback:
        feedback = FeedbackRepository.mark_as_replied(db, feedback_id)
        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback not found")
        return feedback

    @staticmethod
    def list_feedbacks(db: Session, skip: int = 0, limit: int = 100, feedback_reply: Optional[bool] = None):
        return FeedbackRepository.list(db, skip, limit, feedback_reply)

    @staticmethod
    def search_feedbacks_by_email(db: Session, email: str, skip: int = 0, limit: int = 100, feedback_reply: Optional[bool] = None):
        return FeedbackRepository.search_by_email(db, email, skip, limit, feedback_reply)