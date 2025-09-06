from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.v1.deps import get_session
from typing import List, Optional
from app.services.business_service import BusinessService
from app.schemas.business import BusinessCreate, BusinessUpdate, BusinessResponse, PaginatedResponse


router = APIRouter(prefix="/business", tags=["Business"])

# Create
@router.post("/", response_model=BusinessResponse)
def create_business(b: BusinessCreate, db: Session = Depends(get_session)):
    return BusinessService(db).create_business(b)

# List
@router.get("/", response_model=List[BusinessResponse])
def list_businesses(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return BusinessService(db).list_businesses(skip, limit)

# Get by ID
@router.get("/{business_id}", response_model=BusinessResponse)
def get_business(business_id: int, db: Session = Depends(get_session)):
    business = BusinessService(db).get_business(business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business

# Update (PATCH)
@router.patch("/{business_id}", response_model=BusinessResponse)
def update_business(business_id: int, b_update: BusinessUpdate, db: Session = Depends(get_session)):
    return BusinessService(db).update_business(business_id, b_update)

# Search with pagination
@router.get("/search_paginated", response_model=PaginatedResponse)
def search_businesses_paginated(
    company_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    phone: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    db: Session = Depends(get_session)
):
    return BusinessService(db).search_businesses_paginated(
        company_name=company_name,
        email=email,
        phone=phone,
        skip=skip,
        limit=limit
    )
