from sqlalchemy.orm import Session
from app.repositories.item_repo import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate

class ItemService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = ItemRepository(session)

    def create_item(self, payload: ItemCreate):
        item = self.repo.create(title=payload.title, description=payload.description)
        self.session.commit()
        return item

    def get_item(self, item_id: int):
        return self.repo.get(item_id)

    def list_items(self, limit: int = 100, offset: int = 0):
        return self.repo.list(limit=limit, offset=offset)

    def update_item(self, item_id: int, payload: ItemUpdate):
        item = self.repo.update(item_id, title=payload.title, description=payload.description)
        if item:
            self.session.commit()
        return item

    def delete_item(self, item_id: int):
        ok = self.repo.delete(item_id)
        if ok:
            self.session.commit()
        return ok
