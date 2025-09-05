from sqlalchemy.orm import Session
from app.repositories.question_repo import ExpertQuestionRepository
from app.schemas.question import QuestionCreate

class ExpertQuestionService:
    def __init__(self, db: Session):
        self.db = db

    def create_question(self, q: QuestionCreate):
        return ExpertQuestionRepository.create_question(self.db, q)

    def get_question(self, question_id: int):
        return ExpertQuestionRepository.get_question(self.db, question_id)

    def list_questions(self, skip: int = 0, limit: int = 100):
        return ExpertQuestionRepository.list_questions(self.db, skip=skip, limit=limit)

    def list_questions_by_email(self, user_email: str, skip: int = 0, limit: int = 100):
        return ExpertQuestionRepository.list_questions_by_email(self.db, user_email, skip=skip, limit=limit)

    def list_questions_by_answered_email(self, answered_by_email: str, skip: int = 0, limit: int = 100):
        return ExpertQuestionRepository.list_questions_by_answered_email(self.db, answered_by_email, skip=skip, limit=limit)
