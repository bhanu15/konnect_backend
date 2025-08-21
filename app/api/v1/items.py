from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.api.v1.deps import get_session
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, session = Depends(get_session)):
    service = ItemService(session)
    return service.create_item(payload)

@router.get("/{item_id}", response_model=ItemRead)
def read_item(item_id: int, session = Depends(get_session)):
    service = ItemService(session)
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/", response_model=List[ItemRead])
def list_items(limit: int = 100, offset: int = 0, session = Depends(get_session)):
    service = ItemService(session)
    return service.list_items(limit=limit, offset=offset)

@router.patch("/{item_id}", response_model=ItemRead)
def update_item(item_id: int, payload: ItemUpdate, session = Depends(get_session)):
    service = ItemService(session)
    item = service.update_item(item_id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, session = Depends(get_session)):
    service = ItemService(session)
    ok = service.delete_item(item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")
    return None
