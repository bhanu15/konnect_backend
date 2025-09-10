from sqlalchemy.orm import Session
from app.models.business_card import BusinessCard
from app.schemas.business_card_schema import BusinessCardCreate

class BusinessCardRepository:

    @staticmethod
    def create(db: Session, card_data: BusinessCardCreate, file_url: str):
        card = BusinessCard(
            company_name=card_data.company_name,
            phone_number=card_data.phone_number,
            email=card_data.email,
            file_url=file_url,
            is_deleted=False
        )
        db.add(card)
        db.commit()
        db.refresh(card)
        return card

    @staticmethod
    def get_by_id(db: Session, card_id: int):
        return db.query(BusinessCard).filter(
            BusinessCard.id == card_id,
            BusinessCard.is_deleted.is_(False)
        ).first()

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100):
        return db.query(BusinessCard).filter(BusinessCard.is_deleted.is_(False)).offset(skip).limit(limit).all()

    @staticmethod
    def soft_delete(db: Session, card_id: int):
        card = db.query(BusinessCard).filter(BusinessCard.id == card_id).first()
        if not card:
            return None
        card.is_deleted = True
        db.commit()
        return card

    @staticmethod
    def search(db: Session, email: str | None = None, phone_number: str | None = None,
               skip: int = 0, limit: int = 100, sort_by: str = "company_name", sort_order: str = "asc"):
        query = db.query(BusinessCard).filter(BusinessCard.is_deleted.is_(False))

        if email:
            query = query.filter(BusinessCard.email.ilike(f"%{email}%"))
        if phone_number:
            query = query.filter(BusinessCard.phone_number.ilike(f"%{phone_number}%"))

        col = BusinessCard.email if sort_by == "email" else BusinessCard.company_name
        col = col.desc() if sort_order.lower() == "desc" else col.asc()

        return query.order_by(col).offset(skip).limit(limit).all()
