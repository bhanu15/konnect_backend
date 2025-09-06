from fastapi import APIRouter, Depends, HTTPException, Query, Body
from typing import List
from sqlalchemy.orm import Session
from app.api.v1.deps import get_session
from app.services.question_service import ExpertQuestionService
from app.schemas.question import QuestionCreate, QuestionResponse, QuestionUpdate

router = APIRouter(prefix="/questions", tags=["Expert Questions"])

# --------- Create ----------
@router.post("/", response_model=QuestionResponse)
def create_question(q: QuestionCreate, db: Session = Depends(get_session)):
    return ExpertQuestionService(db).create_question(q)

# --------- Read ----------
@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_session)):
    service = ExpertQuestionService(db)
    question = service.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.get("/", response_model=List[QuestionResponse])
def list_questions(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1), db: Session = Depends(get_session)):
    return ExpertQuestionService(db).list_questions(skip=skip, limit=limit)

@router.get("/user/{user_email}", response_model=List[QuestionResponse])
def list_questions_by_email(user_email: str, skip: int = Query(0, ge=0), limit: int = Query(100, ge=1), db: Session = Depends(get_session)):
    return ExpertQuestionService(db).list_questions_by_email(user_email=user_email, skip=skip, limit=limit)

@router.get("/answered-by/{answered_by_email}", response_model=List[QuestionResponse])
def list_questions_by_answered_email(answered_by_email: str, skip: int = Query(0, ge=0), limit: int = Query(100, ge=1), db: Session = Depends(get_session)):
    return ExpertQuestionService(db).list_questions_by_answered_email(answered_by_email=answered_by_email, skip=skip, limit=limit)

# --------- Update ----------
@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(question_id: int, q: QuestionUpdate, answered_by: str = Body(None), db: Session = Depends(get_session)):
    service = ExpertQuestionService(db)
    updated = service.update_question(question_id, q, answered_by=answered_by)
    if not updated:
        raise HTTPException(status_code=404, detail="Question not found")
    return updated

@router.patch("/{question_id}", response_model=QuestionResponse)
def patch_question(question_id: int, q: QuestionUpdate, answered_by: str = Body(None), db: Session = Depends(get_session)):
    service = ExpertQuestionService(db)
    updated = service.update_question(question_id, q, answered_by=answered_by)
    if not updated:
        raise HTTPException(status_code=404, detail="Question not found")
    return updated
