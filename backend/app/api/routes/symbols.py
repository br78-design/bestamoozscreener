from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.symbol import Symbol
from app.schemas.symbol import SymbolResponse

router = APIRouter(prefix="/api/symbols", tags=["symbols"])


@router.get("", response_model=List[SymbolResponse])
def list_symbols(
    search: str = Query(default=""),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Symbol)
    if search:
        query = query.filter(Symbol.symbol.contains(search))
    offset = (page - 1) * page_size
    symbols = query.offset(offset).limit(page_size).all()
    return symbols
