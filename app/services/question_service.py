from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.question_repo import QuestionRepository
from app.schemas.question import QuestionCreate, QuestionUpdate

class ExpertQuestionService:
    def __init__(self, db: Session):
        self.repo = QuestionRepository(db)

    # --------- Create ----------
    def create_question(self, q: QuestionCreate):
        return self.repo.create(q)

    # --------- Read ----------
    def get_question(self, question_id: int):
        return self.repo.get(question_id)

    def list_questions(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip, limit)

    def list_questions_by_email(self, user_email: str, skip: int = 0, limit: int = 100):
        return self.repo.list_by_user(user_email, skip, limit)

    def list_questions_by_answered_email(self, answered_by_email: str, skip: int = 0, limit: int = 100):
        return self.repo.list_by_answered(answered_by_email, skip, limit)

    # --------- Update ----------
    def update_question(self, question_id: int, q_update: QuestionUpdate, answered_by: str = None):
        question = self.repo.get(question_id)
        if not question:
            return None

        update_data = q_update.dict(exclude_unset=True)

        #  Prevent direct edits of answered_by / answered_at
        if "answered_by" in update_data or "answered_at" in update_data:
            raise HTTPException(
                status_code=400,
                detail="answered_by and answered_at cannot be updated directly; update answer instead"
            )

        #  Business rules for answer
        if "answer" in update_data:
            if update_data["answer"] is not None:
                if not answered_by:
                    raise HTTPException(
                        status_code=400,
                        detail="answered_by must be provided when updating the answer"
                    )
                update_data["answered_by"] = answered_by
                update_data["answered_at"] = datetime.utcnow()
            else:
                update_data["answered_by"] = None
                update_data["answered_at"] = None

        return self.repo.update(question, update_data)
