from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
headless: bool = os.getenv("A_HEADLESS", "true").lower() == "true"
region: str = os.getenv("A_REGION", "US")
rate_delay_ms: int = int(os.getenv("A_RATE_DELAY_MS", "2000"))
max_concurrency: int = int(os.getenv("A_MAX_CONCURRENCY", "1"))
user_agent: str = os.getenv(
"A_USER_AGENT",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
)
proxy: str | None = os.getenv("A_PROXY") or None


SETTINGS = Settings()
