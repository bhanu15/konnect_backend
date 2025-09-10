import json
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate

class UserRepository:
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.user_id == user_id, User.is_deleted.is_(False)).first()

    @staticmethod
    def get_by_sub(db: Session, sub: str) -> User | None:
        return db.query(User).filter(User.sub == sub, User.is_deleted.is_(False)).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email, User.is_deleted.is_(False)).first()

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        return (
            db.query(User)
            .filter(User.is_deleted.is_(False))
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create(db: Session, user_data: UserCreate) -> User:
        data = json.loads(user_data.json())
        user = User(**data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update(db: Session, user_id: int, update_data: UserUpdate) -> User | None:
        user = db.query(User).filter(User.user_id == user_id, User.is_deleted.is_(False)).first()
        if not user:
            return None
        update_dict = json.loads(update_data.json(exclude_unset=True))
        for key, value in update_dict.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user_id: int) -> User | None:
        user = db.query(User).filter(User.user_id == user_id, User.is_deleted.is_(False)).first()
        if not user:
            return None
        user.is_deleted = True
        db.commit()
        db.refresh(user)
        return user
