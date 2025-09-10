from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.v1.deps import get_session
from app.services.feedback_service import FeedbackService
from app.schemas.feedback_schema import FeedbackCreate, FeedbackUpdate, FeedbackResponse

router = APIRouter(prefix="/feedbacks", tags=["feedback"])

@router.post("/", response_model=FeedbackResponse)
def create_feedback(
    type: str = Form(...),
    details: str = Form(...),
    user_email: str = Form(...),
    user_id: Optional[int] = Form(None),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_session)
):
    feedback_data = FeedbackCreate(type=type, details=details, user_email=user_email, user_id=user_id)
    return FeedbackService.create_feedback(db, feedback_data, file)

@router.get("/", response_model=List[FeedbackResponse])
def list_feedbacks(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return FeedbackService.list_feedbacks(db, skip, limit)

@router.get("/{feedback_id}", response_model=FeedbackResponse)
def get_feedback(feedback_id: int, db: Session = Depends(get_session)):
    return FeedbackService.get_feedback_by_id(db, feedback_id)

@router.put("/{feedback_id}", response_model=FeedbackResponse)
def update_feedback(
    feedback_id: int,
    type: Optional[str] = Form(None),
    details: Optional[str] = Form(None),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_session)
):
    feedback_update = FeedbackUpdate(type=type, details=details)
    return FeedbackService.update_feedback(db, feedback_id, feedback_update, file)

@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_session)):
    return FeedbackService.delete_feedback(db, feedback_id)

@router.post("/{feedback_id}/reply", response_model=FeedbackResponse)
def mark_as_replied(feedback_id: int, db: Session = Depends(get_session)):
    return FeedbackService.mark_as_replied(db, feedback_id)

@router.get("/search/", response_model=List[FeedbackResponse])
def search_feedbacks_by_email(
    email: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session)
):
    return FeedbackService.search_feedbacks_by_email(db, email, skip, limit)
