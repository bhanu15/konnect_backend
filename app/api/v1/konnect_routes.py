# app/api/v1/konnect_routes.py
import asyncio
import uuid
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.services.konnect_service import KonnectService

router = APIRouter(prefix="/konnect", tags=["Konnect"])
konnect_service = KonnectService()


@router.post("/search")
async def stream_konnect_search(request: Request, payload: dict):
    question = payload.get("searchQuestion")
    if not question:
        return {"error": "Missing 'searchQuestion'"}

    # Allow frontend to provide requestId for polling
    request_id = payload.get("requestId", str(uuid.uuid4()))

    async def event_generator():
        async for chunk in konnect_service.stream_llm_response(question, request_id):
            yield chunk
            await asyncio.sleep(0)  # force flush

    return StreamingResponse(
        event_generator(),
        media_type="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # if using nginx
        },
    )

