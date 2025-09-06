from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.business import Business
from app.schemas.business import BusinessCreate

class BusinessRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, b: BusinessCreate) -> Business:
        new_b = Business(**b.dict())
        self.db.add(new_b)
        self.db.commit()
        self.db.refresh(new_b)
        return new_b

    def get(self, business_id: int) -> Optional[Business]:
        return self.db.query(Business).filter(Business.id == business_id).first()

    def list(self, skip: int = 0, limit: int = 100) -> List[Business]:
        return self.db.query(Business).offset(skip).limit(limit).all()

    def update(self, business: Business, update_data: dict) -> Business:
        for key, value in update_data.items():
            setattr(business, key, value)
        self.db.commit()
        self.db.refresh(business)
        return business

    # Uniqueness helpers
    def get_by_email(self, email: str) -> Optional[Business]:
        return self.db.query(Business).filter(Business.email == email).first()

    def get_by_company_name(self, company_name: str) -> Optional[Business]:
        return self.db.query(Business).filter(Business.company_name == company_name).first()

    # Search with total count
    def search_with_count(
        self,
        company_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ):
        query = self.db.query(Business)
        if company_name:
            query = query.filter(Business.company_name.ilike(f"%{company_name}%"))
        if email:
            query = query.filter(Business.email == email)
        if phone:
            query = query.filter(Business.phone == phone)
        total = query.count()
        results = query.offset(skip).limit(limit).all()
        return total, results
