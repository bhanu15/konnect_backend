from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional
from app.repositories.business_repository import BusinessRepository
from app.schemas.business import BusinessCreate, BusinessUpdate

class BusinessService:
    def __init__(self, db: Session):
        self.repo = BusinessRepository(db)

    def create_business(self, b: BusinessCreate):
        if self.repo.get_by_email(b.email):
            raise HTTPException(status_code=409, detail=f"Business with email '{b.email}' already exists.")
        if self.repo.get_by_company_name(b.company_name):
            raise HTTPException(status_code=409, detail=f"Business with company name '{b.company_name}' already exists.")
        return self.repo.create(b)

    def get_business(self, business_id: int):
        return self.repo.get(business_id)

    def list_businesses(self, skip: int = 0, limit: int = 100) -> List:
        return self.repo.list(skip, limit)

    def update_business(self, business_id: int, b_update: BusinessUpdate):
        business = self.repo.get(business_id)
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")

        update_data = b_update.dict(exclude_unset=True)

        if "email" in update_data and update_data["email"] != business.email:
            if self.repo.get_by_email(update_data["email"]):
                raise HTTPException(status_code=409, detail=f"Business with email '{update_data['email']}' already exists.")
        if "company_name" in update_data and update_data["company_name"] != business.company_name:
            if self.repo.get_by_company_name(update_data["company_name"]):
                raise HTTPException(status_code=409, detail=f"Business with company name '{update_data['company_name']}' already exists.")

        return self.repo.update(business, update_data)

    def search_businesses_paginated(
        self,
        company_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ):
        total, results = self.repo.search_with_count(company_name, email, phone, skip, limit)
        return {"total": total, "skip": skip, "limit": limit, "results": results}
