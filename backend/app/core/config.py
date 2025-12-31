from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "bestamoozscreener"
    database_url: str = "sqlite:///./app.db"
    mock_data_file: str = "backend/seed/symbols_seed.json"
    cache_ttl_seconds: int = 60
    data_provider: str = "tsetmc"
    tsetmc_base_url: str = "https://cdn.tsetmc.com"
    tsetmc_api_prefix: str = "/api"
    tsetmc_max_symbols: int = 120

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
