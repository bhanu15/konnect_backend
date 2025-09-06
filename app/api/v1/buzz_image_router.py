from fastapi import APIRouter, Depends, UploadFile, Form
from sqlalchemy.orm import Session
from app.api.v1.deps import get_session
from app.schemas.buzz_image_schema import BuzzImageOut, BuzzImageUpdate
from app.services.buzz_image_service import BuzzImageService

router = APIRouter(prefix="/buzz-images", tags=["BuzzImages"])


@router.post("/", response_model=BuzzImageOut)
def upload_buzz_image(
    file: UploadFile,
    title: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_session),
):
    return BuzzImageService.save_image(db, file, title, description)


@router.get("/", response_model=list[BuzzImageOut])
def list_buzz_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return BuzzImageService.list_images(db, skip, limit)


@router.get("/{image_id}", response_model=BuzzImageOut)
def get_buzz_image(image_id: int, db: Session = Depends(get_session)):
    return BuzzImageService.get_image_by_id(db, image_id)


@router.put("/{image_id}", response_model=BuzzImageOut)
def update_buzz_image(image_id: int, data: BuzzImageUpdate, db: Session = Depends(get_session)):
    return BuzzImageService.update_image(db, image_id, data.title, data.description)


@router.delete("/{image_id}")
def delete_buzz_image(image_id: int, db: Session = Depends(get_session)):
    return BuzzImageService.delete_image(db, image_id)
