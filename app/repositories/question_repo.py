from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.question import ExpertQuestion
from app.schemas.question import QuestionCreate, QuestionUpdate

class QuestionRepository:
    def __init__(self, db: Session):
        self.db = db

    # --------- Create ----------
    def create(self, q: QuestionCreate) -> ExpertQuestion:
        new_q = ExpertQuestion(
            question_text=q.question_text,
            asked_by=q.asked_by
        )
        self.db.add(new_q)
        self.db.commit()
        self.db.refresh(new_q)
        return new_q

    # --------- Read ----------
    def get(self, question_id: int) -> Optional[ExpertQuestion]:
        return self.db.query(ExpertQuestion).filter(ExpertQuestion.id == question_id).first()

    def list(self, skip: int = 0, limit: int = 100) -> List[ExpertQuestion]:
        return (
            self.db.query(ExpertQuestion)
            .order_by(ExpertQuestion.asked_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def list_by_user(self, user_email: str, skip: int = 0, limit: int = 100) -> List[ExpertQuestion]:
        return (
            self.db.query(ExpertQuestion)
            .filter(ExpertQuestion.asked_by == user_email)
            .order_by(ExpertQuestion.asked_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def list_by_answered(self, answered_by_email: str, skip: int = 0, limit: int = 100) -> List[ExpertQuestion]:
        return (
            self.db.query(ExpertQuestion)
            .filter(ExpertQuestion.answered_by == answered_by_email)
            .order_by(ExpertQuestion.asked_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    # --------- Update ----------
    def update(self, question: ExpertQuestion, update_data: dict) -> ExpertQuestion:
        for key, value in update_data.items():
            setattr(question, key, value)
        self.db.commit()
        self.db.refresh(question)
        return question
