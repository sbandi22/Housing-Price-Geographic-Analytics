"""Data cleaning and normalization.

Reads staging tables, applies cleaning rules, derives features,
and writes final 3NF tables.
"""
import logging
import numpy as np
import pandas as pd
from sqlalchemy import text

from src.utils.db import get_engine

log = logging.getLogger('preprocess')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def _winsorize(s: pd.Series, lower=0.01, upper=0.99) -> pd.Series:
    lo, hi = s.quantile([lower, upper])
    return s.clip(lower=lo, upper=hi)


def clean_listings() -> pd.DataFrame:
    eng = get_engine()
    df = pd.read_sql('SELECT * FROM stg_housing_listings', eng)
    log.info('Loaded %d staging listings', len(df))

    # Standardize types
    df['sale_price']  = pd.to_numeric(df.get('sale_price'),  errors='coerce')
    df['list_price']  = pd.to_numeric(df.get('list_price'),  errors='coerce')
    df['sqft_living'] = pd.to_numeric(df.get('sqft_living'), errors='coerce')
    df['bedrooms']    = pd.to_numeric(df.get('bedrooms'),    errors='coerce')
    df['bathrooms']   = pd.to_numeric(df.get('bathrooms'),   errors='coerce')

    # Drop impossible rows
    df = df.dropna(subset=['sale_price', 'sqft_living'])
    df = df[(df['sale_price'] > 10_000) & (df['sqft_living'] > 100)]

    # Winsorize numeric outliers
    for col in ('sale_price', 'sqft_living', 'sqft_lot'):
        if col in df:
            df[col] = _winsorize(df[col].astype(float))

    # Derived features
    df['price_per_sqft'] = df['sale_price'] / df['sqft_living']
    df['property_age']   = pd.to_datetime('today').year - df['year_built'].astype('Int64')
    df['log_price']      = np.log1p(df['sale_price'])

    df.to_sql('fact_housing_listing_clean', eng, if_exists='replace', index=False)
    log.info('Wrote %d cleaned rows', len(df))
    return df


def clean_demographics() -> pd.DataFrame:
    eng = get_engine()
    df = pd.read_sql('SELECT * FROM stg_demographics', eng)
    df = df.dropna(subset=['zip_code'])
    for c in ('median_household_income', 'population_density', 'pct_owner_occupied'):
        if c in df:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    df.to_sql('fact_demographics_clean', eng, if_exists='replace', index=False)
    log.info('Wrote %d demographic rows', len(df))
    return df


def run() -> None:
    log.info('=== Preprocess start ===')
    clean_listings()
    clean_demographics()
    log.info('=== Preprocess complete ===')


if __name__ == '__main__':
    run()
