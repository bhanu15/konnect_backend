from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.item import Item

class ItemRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, title: str, description: Optional[str] = None) -> Item:
        item = Item(title=title, description=description)
        self.session.add(item)
        self.session.flush()
        return item

    def get(self, item_id: int) -> Optional[Item]:
        return self.session.get(Item, item_id)

    def list(self, limit: int = 100, offset: int = 0) -> List[Item]:
        return self.session.query(Item).limit(limit).offset(offset).all()

    def update(self, item_id: int, **kwargs) -> Optional[Item]:
        obj = self.get(item_id)
        if not obj:
            return None
        for k, v in kwargs.items():
            if v is not None:
                setattr(obj, k, v)
        self.session.flush()
        return obj

    def delete(self, item_id: int) -> bool:
        obj = self.get(item_id)
        if not obj:
            return False
        self.session.delete(obj)
        return True
