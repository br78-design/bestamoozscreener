import json
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.symbol import Symbol


def init_db(session: Session) -> None:
    settings = get_settings()
    seed_path = Path(settings.mock_data_file)
    if not seed_path.exists():
        raise FileNotFoundError(f"Seed file not found: {seed_path}")

    existing = session.query(Symbol).count()
    if existing > 0:
        return

    with seed_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        symbol = Symbol(
            symbol=item["symbol"],
            company_name=item["company_name"],
            last_price=item["last_price"],
            volume=item["volume"],
            trade_value=item["trade_value"],
            percent_change=item["percent_change"],
            last_updated=datetime.fromisoformat(item["last_updated"]),
        )
        session.add(symbol)
    session.commit()
