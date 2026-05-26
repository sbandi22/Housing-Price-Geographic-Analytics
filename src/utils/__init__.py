"""Shared utilities: config and DB connection."""
from .config import DB, MODEL  # noqa: F401
from .db import get_engine, session_scope  # noqa: F401
