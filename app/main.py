from fastapi import FastAPI
from app.core.config import settings
from app.logger import configure_logging
from app.middleware import RequestLoggingMiddleware
from app.api.v1 import items
from app.db.session import create_db_and_tables

def create_app() -> FastAPI:
    configure_logging(settings.LOG_LEVEL)
    app = FastAPI(title=settings.APP_NAME)
    app.add_middleware(RequestLoggingMiddleware)
    app.include_router(items.router, prefix="/api/v1")

    @app.on_event("startup")
    def on_startup():
        if settings.DATABASE_URL:  # Only auto-create in dev/test
            create_db_and_tables()

    return app

app = create_app()
