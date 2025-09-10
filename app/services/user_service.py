from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate

class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return UserRepository.get_by_id(db, user_id)

    @staticmethod
    def get_user_by_sub(db: Session, sub: str):
        return UserRepository.get_by_sub(db, sub)

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return UserRepository.get_by_email(db, email)

    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 100):
        return UserRepository.list(db, skip, limit)

    @staticmethod
    def create_user(db: Session, user_data: UserCreate):
        return UserRepository.create(db, user_data)

    @staticmethod
    def update_user(db: Session, user_id: int, update_data: UserUpdate):
        return UserRepository.update(db, user_id, update_data)

    @staticmethod
    def delete_user(db: Session, user_id: int):
        return UserRepository.delete(db, user_id)
