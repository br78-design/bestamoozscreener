from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api.routes import filters, screener, symbols
from app.core.config import get_settings
from app.db import session as db_session
from app.db.init_db import init_db
from app.models import base as models_base

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(filters.router)
app.include_router(symbols.router)
app.include_router(screener.router)


@app.on_event("startup")
def on_startup():
    models_base.Base.metadata.create_all(bind=db_session.engine)
    db: Session = db_session.SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}
