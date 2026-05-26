"""Unit tests for analytics functions."""
import numpy as np
import pandas as pd
import pytest

from src.analytics.stats import describe, detect_outliers_iqr, t_test
from src.analytics.correlation import pearson_matrix, target_correlations, PRICE_DRIVERS
from src.analytics.geo_analysis import add_distance_to_point, hotspot_score


@pytest.fixture
def sample():
    rng = np.random.default_rng(42)
    n = 300
    return pd.DataFrame({
        'sale_price':  rng.lognormal(12.5, 0.4, n),
        'sqft_living': rng.integers(700, 4000, n),
        'bedrooms':    rng.integers(1, 6, n),
        'bathrooms':   rng.choice([1, 1.5, 2, 2.5, 3], n),
        'year_built':  rng.integers(1950, 2024, n),
        'median_household_income': rng.normal(85000, 25000, n),
        'zip_code':    rng.choice(['10001', '90001', '94110', '02139'], n),
        'latitude':    rng.uniform(25, 49, n),
        'longitude':   rng.uniform(-124, -67, n),
    })


def test_describe(sample):
    s = describe(sample['sale_price'])
    assert s.n == 300
    assert s.mean > 0
    assert s.std > 0
    assert s.q3 > s.q1


def test_outlier_detection(sample):
    flags = detect_outliers_iqr(sample['sale_price'])
    assert flags.dtype == bool
    assert 0 < flags.sum() < len(sample)


def test_correlation_shape(sample):
    m = pearson_matrix(sample)
    assert m.shape[0] == m.shape[1]


def test_target_corr(sample):
    tc = target_correlations(sample, 'sale_price')
    assert 'pearson_r' in tc.columns
    assert (tc['pearson_r'].abs() <= 1).all()


def test_distance(sample):
    out = add_distance_to_point(sample.copy(), lat=40.0, lon=-100.0)
    assert 'distance_to_cbd_km' in out.columns
    assert (out['distance_to_cbd_km'] >= 0).all()


def test_hotspot(sample):
    res = hotspot_score(sample)
    assert 'classification' in res.columns
    assert res['zscore'].abs().max() < 10


def test_t_test(sample):
    a = sample.loc[sample['bedrooms'] <= 2, 'sale_price']
    b = sample.loc[sample['bedrooms'] >= 3, 'sale_price']
    out = t_test(a, b)
    assert 'p_value' in out
    assert 0 <= out['p_value'] <= 1
