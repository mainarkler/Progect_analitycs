"""Configuration module."""

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "analytics-refactor")
    app_env: str = os.getenv("APP_ENV", "local")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    moex_base_url: str = os.getenv("MOEX_BASE_URL", "https://iss.moex.com")
    cbr_base_url: str = os.getenv("CBR_BASE_URL", "https://www.cbr.ru")
    http_timeout_seconds: float = float(os.getenv("HTTP_TIMEOUT_SECONDS", "5"))
    http_retry_count: int = int(os.getenv("HTTP_RETRY_COUNT", "3"))
    http_retry_backoff_seconds: float = float(os.getenv("HTTP_RETRY_BACKOFF_SECONDS", "0.5"))
