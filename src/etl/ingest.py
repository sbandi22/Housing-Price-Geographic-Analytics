"""Data ingestion pipeline.

Reads raw CSV / GeoJSON files from data/raw and loads them into
the PostgreSQL warehouse (staging tables).
"""
import logging
from pathlib import Path

import pandas as pd
import geopandas as gpd
from sqlalchemy import text

from src.utils.config import RAW_DIR, EXTERNAL_DIR
from src.utils.db import get_engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger('ingest')


def load_csv(filename: str, table: str, if_exists: str = 'replace') -> int:
    """Load a CSV from data/raw into a staging table. Returns row count."""
    path = RAW_DIR / filename
    if not path.exists():
        log.warning('File not found: %s', path)
        return 0
    df = pd.read_csv(path)
    df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]
    eng = get_engine()
    df.to_sql(f'stg_{table}', eng, if_exists=if_exists, index=False, schema='public')
    log.info('Loaded %d rows into stg_%s', len(df), table)
    return len(df)


def load_geojson(filename: str, table: str) -> int:
    path = EXTERNAL_DIR / filename
    if not path.exists():
        log.warning('Geo file not found: %s', path)
        return 0
    gdf = gpd.read_file(path).to_crs(epsg=4326)
    eng = get_engine()
    gdf.to_postgis(f'stg_{table}', eng, if_exists='replace', index=False)
    log.info('Loaded %d geometries into stg_%s', len(gdf), table)
    return len(gdf)


def run() -> None:
    log.info('=== Ingestion start ===')
    load_csv('sample_housing.csv',      'housing_listings')
    load_csv('sample_demographics.csv', 'demographics')
    load_csv('sample_economic.csv',     'economic_indicators')
    load_geojson('us_states.geojson',   'us_states')
    log.info('=== Ingestion complete ===')


if __name__ == '__main__':
    run()
