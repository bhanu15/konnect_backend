from fastapi import APIRouter, Depends, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
import mimetypes

from app.schemas.image_schema import ImageOut, ImageUpdate
from app.services.image_service import image_service, UPLOAD_DIR
from fastapi.responses import StreamingResponse
from app.api.v1.deps import get_session

router = APIRouter(prefix="/buzz", tags=["buzz"])


@router.post("/", response_model=ImageOut)
def upload_image(file: UploadFile, description: str = Form(None), db: Session = Depends(get_session)):
    return image_service.upload_image(db, file, description)

@router.get("/{image_id}", response_model=ImageOut)
def get_image(image_id: int, db: Session = Depends(get_session)):
    obj = image_service.get_image(db, image_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Image not found")
    return obj

@router.get("/", response_model=List[ImageOut])
def list_images(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    return image_service.list_images(db, skip, limit)

@router.put("/{image_id}", response_model=ImageOut)
def update_image(image_id: int, update_data: ImageUpdate, db: Session = Depends(get_session)):
    obj = image_service.update_image(db, image_id, update_data)
    if not obj:
        raise HTTPException(status_code=404, detail="Image not found")
    return obj

@router.delete("/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_session)):
    obj = image_service.delete_image(db, image_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"detail": "Image deleted"}

# ✅ File-serving endpoint
@router.get("/files/{filename}")
def serve_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    def iterfile(path: str):
        with open(path, mode="rb") as f:
            while chunk := f.read(1024 * 1024):  # ✅ stream in 1MB chunks
                yield chunk

    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "application/octet-stream"

    return StreamingResponse(iterfile(file_path), media_type=mime_type)
