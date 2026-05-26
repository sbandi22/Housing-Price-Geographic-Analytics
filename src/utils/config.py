"""Centralized configuration loaded from environment variables."""
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR     = PROJECT_ROOT / 'data'
RAW_DIR      = DATA_DIR / 'raw'
INTERIM_DIR  = DATA_DIR / 'interim'
PROCESSED_DIR = DATA_DIR / 'processed'
EXTERNAL_DIR  = DATA_DIR / 'external'
REPORTS_DIR   = PROJECT_ROOT / 'reports'
MODELS_DIR    = PROJECT_ROOT / 'models' / 'artifacts'

for _d in (RAW_DIR, INTERIM_DIR, PROCESSED_DIR, EXTERNAL_DIR, REPORTS_DIR, MODELS_DIR):
    _d.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class DBConfig:
    host: str = os.getenv('DB_HOST', 'localhost')
    port: int = int(os.getenv('DB_PORT', '5432'))
    name: str = os.getenv('DB_NAME', 'housing')
    user: str = os.getenv('DB_USER', 'housing_admin')
    password: str = os.getenv('DB_PASSWORD', 'housing_pass')

    @property
    def url(self) -> str:
        return (
            f'postgresql+psycopg2://{self.user}:{self.password}'
            f'@{self.host}:{self.port}/{self.name}'
        )


@dataclass(frozen=True)
class ModelConfig:
    random_state: int = 42
    test_size: float = 0.2
    n_estimators: int = 400
    max_depth: int = 12
    learning_rate: float = 0.05


DB     = DBConfig()
MODEL  = ModelConfig()
