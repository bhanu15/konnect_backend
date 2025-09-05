from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.deps import get_session
from app.services.feature_toggle_service import FeatureToggleService
from app.schemas.feature_toggle_schema import (
FeatureToggleCreate,
FeatureToggleUpdate,
FeatureToggleOut,
)


router = APIRouter(prefix="/features", tags=["Feature Toggles"])


@router.get("/", response_model=list[FeatureToggleOut])
def list_features(db: Session = Depends(get_session)):
	return FeatureToggleService.list_toggles(db)


@router.post("/", response_model=FeatureToggleOut, status_code=status.HTTP_201_CREATED)
def create_feature(data: FeatureToggleCreate, db: Session = Depends(get_session)):
	try:
		return FeatureToggleService.create_toggle(db, data)
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{name}", response_model=FeatureToggleOut)
def update_feature(name: str, data: FeatureToggleUpdate, db: Session = Depends(get_session)):
	updated = FeatureToggleService.update_toggle(db, name, data)
	if not updated:
		raise HTTPException(status_code=404, detail="Feature not found")
	return updated


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_feature(name: str, db: Session = Depends(get_session)):
	ok = FeatureToggleService.delete_toggle(db, name)
	if not ok:
		raise HTTPException(status_code=404, detail="Feature not found")
	return None


@router.get("/is_enabled/{name}")
def is_feature_enabled(name: str, db: Session = Depends(get_session)):
	return {"name": name, "enabled": FeatureToggleService.is_enabled(db, name)}