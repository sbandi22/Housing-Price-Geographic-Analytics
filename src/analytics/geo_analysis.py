"""Geographic / geospatial analytics.

Includes:
  * Aggregations by state / county / ZIP
  * Distance-to-CBD feature engineering
  * Moran's I-style spatial autocorrelation (approximate)
"""
from pathlib import Path
from typing import Tuple

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point


def aggregate_by_region(df: pd.DataFrame, region_col: str,
                        price_col: str = 'sale_price') -> pd.DataFrame:
    return (
        df.groupby(region_col)
          .agg(sales=(price_col, 'count'),
               avg_price=(price_col, 'mean'),
               median_price=(price_col, 'median'),
               std_price=(price_col, 'std'))
          .reset_index()
          .sort_values('avg_price', ascending=False)
    )


def add_distance_to_point(df: pd.DataFrame, lat: float, lon: float,
                          new_col: str = 'distance_to_cbd_km') -> pd.DataFrame:
    """Haversine distance (km) from each row to a reference point."""
    R = 6371.0
    lat1 = np.radians(df['latitude'].astype(float))
    lon1 = np.radians(df['longitude'].astype(float))
    lat2 = np.radians(lat)
    lon2 = np.radians(lon)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    df[new_col] = 2 * R * np.arcsin(np.sqrt(a))
    return df


def to_geodataframe(df: pd.DataFrame, lat='latitude', lon='longitude') -> gpd.GeoDataFrame:
    geom = [Point(xy) for xy in zip(df[lon], df[lat])]
    return gpd.GeoDataFrame(df.copy(), geometry=geom, crs='EPSG:4326')


def moran_i_approx(values: np.ndarray, neighbors: np.ndarray) -> float:
    """Simple Moran's I given a binary neighbor matrix (n x n)."""
    n = len(values)
    m = values - values.mean()
    w_sum = neighbors.sum()
    if w_sum == 0:
        return float('nan')
    num = (neighbors * np.outer(m, m)).sum()
    den = (m ** 2).sum()
    return float((n / w_sum) * (num / den))


def hotspot_score(df: pd.DataFrame, price_col: str = 'sale_price') -> pd.DataFrame:
    """Rank ZIPs by a simple z-score of average price = 'hot' vs 'cold'."""
    agg = df.groupby('zip_code')[price_col].mean().reset_index()
    agg['zscore'] = (agg[price_col] - agg[price_col].mean()) / agg[price_col].std()
    agg['classification'] = pd.cut(
        agg['zscore'],
        bins=[-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf],
        labels=['Cold', 'Cool', 'Neutral', 'Warm', 'Hot']
    )
    return agg.sort_values('zscore', ascending=False)
