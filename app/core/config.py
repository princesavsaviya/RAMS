from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_ENV: str = "local"
    APP_PORT: int = 8000
    APP_API_KEY: str = "later"
    RETENTION_POINTS: int = 10000
    DEFAULT_WINDOW: int = 3600
    CACHE_TTL_SECONDS: int = 2
    LOG_LEVEL: str = "INFO"
    
    # Forex specific
    SYMBOLS: List[str] = [
        "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", 
        "USDCAD", "USDCHF", "USDINR", "EURINR"
    ]
    BAR_FREQUENCY: str = "1s"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
