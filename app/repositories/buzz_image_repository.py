from sqlalchemy.orm import Session
from app.models.buzz_image_model import BuzzImage


class BuzzImageRepository:
    @staticmethod
    def create(db: Session, title: str, description: str | None, url: str) -> BuzzImage:
        obj = BuzzImage(title=title, description=description, url=url)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def get(db: Session, image_id: int) -> BuzzImage | None:
        return db.query(BuzzImage).filter(
            BuzzImage.id == image_id, BuzzImage.is_deleted.is_(False)
        ).first()

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100) -> list[BuzzImage]:
        return (
            db.query(BuzzImage)
            .filter(BuzzImage.is_deleted.is_(False))
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update(
        db: Session, image: BuzzImage, title: str | None, description: str | None
    ) -> BuzzImage:
        if title is not None:
            setattr(image, "title", title)
        if description is not None:
            setattr(image, "description", description)
        db.commit()
        db.refresh(image)
        return image

    @staticmethod
    def soft_delete(db: Session, image: BuzzImage):
        setattr(image, "is_deleted", True)
        db.commit()
