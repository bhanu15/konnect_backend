from sqlalchemy.orm import Session
from app.models.answer import Answer

class AnswerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, query_id: int, answer_text: str):
        answer = Answer(query_id=query_id, answer_text=answer_text)
        self.db.add(answer)
        self.db.commit()
        self.db.refresh(answer)
        return answer
