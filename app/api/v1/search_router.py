from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.api.v1.deps import get_session
from app.schemas.user_search_query import UserSearchQueryCreate
from app.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["search"])

@router.post("/", response_model=dict)
def search(query_in: UserSearchQueryCreate, db: Session = Depends(get_session), request = Request):
    service = SearchService(db)
    result = service.search(query_in, request)
    return result.dict()
