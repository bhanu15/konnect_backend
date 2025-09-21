from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.logger import configure_logging
from app.middleware import RequestLoggingMiddleware
from app.api.v1 import items, feature_toggle_routes, question_routes, buzz_image_router, business_routes, user_router, feedback_router, business_card_router, assistant_router, search_router, konnect_routes

from app.db.session import create_db_and_tables


def create_app() -> FastAPI:
    configure_logging(settings.LOG_LEVEL)
    app = FastAPI(title=settings.APP_NAME or "FastAPI Application")
    # app.add_middleware(RequestLoggingMiddleware)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(feature_toggle_routes.router, prefix="/api/v1")
    app.include_router(question_routes.router, prefix="/api/v1")
    app.include_router(buzz_image_router.router, prefix="/api/v1")
    app.include_router(business_routes.router, prefix="/api/v1")
    app.include_router(user_router.router, prefix="/api/v1")
    app.include_router(feedback_router.router, prefix="/api/v1")
    app.include_router(business_card_router.router, prefix="/api/v1")
    app.include_router(assistant_router.router, prefix="/api/v1")
    app.include_router(search_router.router, prefix="/api/v1")
    app.include_router(konnect_routes.router, prefix="/api/v1")
    
    @app.on_event("startup")
    def on_startup():
        if settings.DATABASE_URL:  # Only auto-create in dev/test
            create_db_and_tables()
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = [{"field": ".".join(str(loc) for loc in err.get("loc", [])), "message": err.get("msg")}
              for err in exc.errors()]
        return JSONResponse(status_code=422, content={"detail": errors})

    

    return app

app = create_app()
