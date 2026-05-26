"""Correlation analysis: Pearson, Spearman, and partial correlations."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

from src.utils.config import REPORTS_DIR

PRICE_DRIVERS = [
    'sale_price', 'sqft_living', 'bedrooms', 'bathrooms', 'year_built',
    'property_age', 'lot_size', 'hoa_fee_monthly', 'days_on_market',
    'median_household_income', 'unemployment_rate', 'population_density',
    'pct_owner_occupied', 'school_score', 'crime_index',
    'walk_score', 'mortgage_rate_30yr', 'months_supply',
]


def pearson_matrix(df: pd.DataFrame, cols: list[str] | None = None) -> pd.DataFrame:
    cols = cols or [c for c in PRICE_DRIVERS if c in df.columns]
    return df[cols].corr(method='pearson')


def spearman_matrix(df: pd.DataFrame, cols: list[str] | None = None) -> pd.DataFrame:
    cols = cols or [c for c in PRICE_DRIVERS if c in df.columns]
    return df[cols].corr(method='spearman')


def target_correlations(df: pd.DataFrame, target: str = 'sale_price') -> pd.DataFrame:
    cols = [c for c in PRICE_DRIVERS if c in df.columns and c != target]
    rows = []
    for c in cols:
        pair = df[[target, c]].dropna()
        if len(pair) < 30:
            continue
        r_p, p_p = stats.pearsonr(pair[target], pair[c])
        r_s, p_s = stats.spearmanr(pair[target], pair[c])
        rows.append({'feature': c, 'pearson_r': r_p, 'pearson_p': p_p,
                     'spearman_r': r_s, 'spearman_p': p_s})
    return pd.DataFrame(rows).sort_values('pearson_r', key=lambda s: s.abs(), ascending=False)


def plot_heatmap(corr: pd.DataFrame, title: str = 'Correlation Matrix',
                 out: str = 'correlation_matrix.png') -> Path:
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
                square=True, cbar_kws={'shrink': 0.8}, ax=ax)
    ax.set_title(title, fontsize=14, weight='bold')
    fig.tight_layout()
    path = REPORTS_DIR / out
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path
