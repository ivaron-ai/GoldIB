"""Configuration management for Ralph."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    """Application configuration."""
    
    database_url: str
    redis_url: str
    host: str
    port: int
    log_level: str

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        load_dotenv()
        
        return cls(
            database_url=os.getenv(
                "DATABASE_URL",
                "postgresql://ralph:ralph_secret@localhost:5432/ralph_db"
            ),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379"),
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )
