from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import ValidationError
from app.api.v1.deps import get_session
from app.schemas.business_card_schema import BusinessCardCreate, BusinessCardResponse
from app.services.business_card_service import BusinessCardService

router = APIRouter(prefix="/business-cards", tags=["business_cards"])

@router.post("/", response_model=BusinessCardResponse)
def create_business_card(
    company_name: str = Form(...),
    phone_number: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_session)
):
    # Validate form data BEFORE S3 upload
    try:
        card_data = BusinessCardCreate(
            company_name=company_name,
            phone_number=phone_number,
            email=email
        )
    except ValidationError as e:
        errors = [{"field": ".".join(str(loc) for loc in err.get("loc", [])), "message": err.get("msg")}
                  for err in e.errors()]
        raise HTTPException(status_code=422, detail=errors)

    return BusinessCardService.create_card(db, card_data, file)

@router.get("/", response_model=List[BusinessCardResponse])
def list_business_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return BusinessCardService.list_cards(db, skip, limit)

@router.get("/{card_id}", response_model=BusinessCardResponse)
def get_business_card(card_id: int, db: Session = Depends(get_session)):
    return BusinessCardService.get_card(db, card_id)

@router.delete("/{card_id}")
def delete_business_card(card_id: int, db: Session = Depends(get_session)):
    return BusinessCardService.delete_card(db, card_id)

@router.get("/search/", response_model=List[BusinessCardResponse])
def search_business_cards(
    email: str | None = None,
    phone_number: str | None = None,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "company_name",   # "company_name" or "email"
    sort_order: str = "asc",         # "asc" or "desc"
    db: Session = Depends(get_session)
):
    if not email and not phone_number:
        raise HTTPException(status_code=400, detail="At least one of email or phone_number is required")
    if sort_by not in ("company_name", "email"):
        raise HTTPException(status_code=400, detail="sort_by must be 'company_name' or 'email'")
    if sort_order.lower() not in ("asc", "desc"):
        raise HTTPException(status_code=400, detail="sort_order must be 'asc' or 'desc'")
    return BusinessCardService.search_cards(
        db,
        email=email,
        phone_number=phone_number,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )
