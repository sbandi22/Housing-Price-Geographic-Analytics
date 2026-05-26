"""Database connection helpers using SQLAlchemy."""
from contextlib import contextmanager
from typing import Iterator
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from .config import DB

_engine: Engine | None = None
_SessionLocal = None


def get_engine() -> Engine:
    global _engine, _SessionLocal
    if _engine is None:
        _engine = create_engine(DB.url, pool_pre_ping=True, pool_size=5, max_overflow=10)
        _SessionLocal = sessionmaker(bind=_engine, expire_on_commit=False)
    return _engine


@contextmanager
def session_scope() -> Iterator[Session]:
    """Yield a transactional session and roll back on error."""
    get_engine()
    session = _SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def run_sql_file(path: str) -> None:
    """Execute every statement in a .sql file."""
    eng = get_engine()
    with open(path, 'r', encoding='utf-8') as f:
        sql = f.read()
    with eng.begin() as conn:
        for stmt in [s.strip() for s in sql.split(';') if s.strip()]:
            conn.execute(text(stmt))
