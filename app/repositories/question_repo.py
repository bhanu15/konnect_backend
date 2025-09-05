from sqlalchemy.orm import Session
from datetime import datetime
from app.models.question import ExpertQuestion
from app.schemas.question import QuestionCreate

class ExpertQuestionRepository:
    @staticmethod
    def create_question(db: Session, q: QuestionCreate):
        db_q = ExpertQuestion(
            user_email=q.user_email,
            question=q.question,
            answer=q.answer,
            answered_by_email=q.answered_by_email,
            asked_at=datetime.utcnow(),
            # answered_at=datetime.utcnow() if q.answer else None
        )
        db.add(db_q)
        db.commit()
        db.refresh(db_q)
        return db_q

    @staticmethod
    def get_question(db: Session, question_id: int):
        return db.query(ExpertQuestion).filter(ExpertQuestion.id == question_id).first()

    @staticmethod
    def list_questions(db: Session, skip: int = 0, limit: int = 100):
        return db.query(ExpertQuestion).offset(skip).limit(limit).all()

    @staticmethod
    def list_questions_by_email(db: Session, user_email: str, skip: int = 0, limit: int = 100):
        return db.query(ExpertQuestion).filter(ExpertQuestion.user_email == user_email).offset(skip).limit(limit).all()

    @staticmethod
    def list_questions_by_answered_email(db: Session, answered_by_email: str, skip: int = 0, limit: int = 100):
        return db.query(ExpertQuestion).filter(ExpertQuestion.answered_by_email == answered_by_email).offset(skip).limit(limit).all()
