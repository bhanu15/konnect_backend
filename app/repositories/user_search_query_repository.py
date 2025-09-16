from sqlalchemy.orm import Session
from app.models.user_search_query import UserSearchQuery

class UserSearchQueryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, search_question, user_email, user_location=None, user_nationality=None, thread_id=None):
        query = UserSearchQuery(
            search_question=search_question,
            user_email=user_email,
            user_location=user_location,
            user_nationality=user_nationality,
            thread_id=thread_id
        )
        self.db.add(query)
        self.db.commit()
        self.db.refresh(query)
        return query

    def get_by_email(self, email: str):
        return self.db.query(UserSearchQuery).filter(UserSearchQuery.user_email == email).all()
