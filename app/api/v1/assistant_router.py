from fastapi import APIRouter, HTTPException
from app.services.assistant_service import assistant_service

router = APIRouter(prefix="/assistant", tags=["assistant"])

@router.post("/create")
def create_assistant(name: str = "DefaultAssistant", description: str = "Default assistant"):
    try:
        assistant_id = assistant_service.create_assistant(name=name, description=description)
        return {"assistant_id": assistant_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_assistant():
    try:
        return {"assistant_id": assistant_service.get_assistant_id()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
