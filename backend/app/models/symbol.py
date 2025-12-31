from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime

from app.models.base import Base


class Symbol(Base):
    __tablename__ = "symbols"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    company_name = Column(String, nullable=False)
    last_price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    trade_value = Column(Float, nullable=False)
    percent_change = Column(Float, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow)
