from sqlalchemy.orm import Session
from app.models.feedback import Feedback
from app.schemas.feedback_schema import FeedbackCreate, FeedbackUpdate

class FeedbackRepository:

    @staticmethod
    def create(db: Session, feedback_data: FeedbackCreate, file_url: str | None):
        feedback = Feedback(
            type=feedback_data.type,
            details=feedback_data.details,
            user_email=feedback_data.user_email,
            user_id=feedback_data.user_id,
            file_url=file_url,
            feedback_reply=False,
            is_deleted=False,
        )
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        return feedback

    @staticmethod
    def get_by_id(db: Session, feedback_id: int):
        return db.query(Feedback).filter(
            Feedback.id == feedback_id,
            Feedback.is_deleted.is_(False)
        ).first()

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Feedback).filter(
            Feedback.is_deleted.is_(False)
        ).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, feedback_id: int, feedback_update: FeedbackUpdate, file_url: str | None):
        feedback = db.query(Feedback).filter(
            Feedback.id == feedback_id,
            Feedback.is_deleted.is_(False)
        ).first()
        if not feedback:
            return None

        feedback.type = feedback_update.type or feedback.type
        feedback.details = feedback_update.details or feedback.details
        if file_url:
            feedback.file_url = file_url

        db.commit()
        db.refresh(feedback)
        return feedback

    @staticmethod
    def soft_delete(db: Session, feedback_id: int):
        feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
        if not feedback:
            return None
        feedback.is_deleted = True
        db.commit()
        return feedback

    @staticmethod
    def mark_as_replied(db: Session, feedback_id: int):
        feedback = db.query(Feedback).filter(
            Feedback.id == feedback_id,
            Feedback.is_deleted.is_(False)
        ).first()
        if not feedback:
            return None
        feedback.feedback_reply = True
        db.commit()
        db.refresh(feedback)
        return feedback

    @staticmethod
    def search_by_email(db: Session, email: str, skip: int = 0, limit: int = 100):
        return db.query(Feedback).filter(
            Feedback.user_email == email,
            Feedback.is_deleted.is_(False)
        ).offset(skip).limit(limit).all()
