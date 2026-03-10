import os
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

# ---------------------------------------------------------------------------
# Database URL handling with prefixing and SSL configuration
# ---------------------------------------------------------------------------
_raw_url = os.getenv("DATABASE_URL", os.getenv("POSTGRES_URL", "sqlite:///./app.db"))
if _raw_url.startswith("postgresql+asyncpg://"):
    _raw_url = _raw_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
elif _raw_url.startswith("postgres://"):
    _raw_url = _raw_url.replace("postgres://", "postgresql+psycopg://")

# Determine if we need SSL (non‑localhost & not SQLite)
_connect_args = {}
if not _raw_url.startswith("sqlite") and "localhost" not in _raw_url and "127.0.0.1" not in _raw_url:
    _connect_args["sslmode"] = "require"

engine = create_engine(_raw_url, connect_args=_connect_args, future=True)
Base = declarative_base()

class MoodEntry(Base):
    __tablename__ = "mm_mood_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, nullable=False)
    emoji = Column(String, nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
