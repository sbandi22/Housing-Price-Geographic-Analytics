"""Statistical analysis utilities for housing data."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd
from scipy import stats


@dataclass
class DescriptiveSummary:
    n: int
    mean: float
    median: float
    std: float
    skewness: float
    kurtosis: float
    q1: float
    q3: float
    iqr: float


def describe(series: pd.Series) -> DescriptiveSummary:
    s = series.dropna().astype(float)
    q1, q3 = s.quantile([0.25, 0.75])
    return DescriptiveSummary(
        n=int(s.size),
        mean=float(s.mean()),
        median=float(s.median()),
        std=float(s.std()),
        skewness=float(stats.skew(s)),
        kurtosis=float(stats.kurtosis(s)),
        q1=float(q1),
        q3=float(q3),
        iqr=float(q3 - q1),
    )


def groupwise_summary(df: pd.DataFrame, group_col: str, value_col: str) -> pd.DataFrame:
    """Return per-group descriptive stats and 95% CI for the mean."""
    rows: List[Dict] = []
    for grp, sub in df.groupby(group_col):
        s = sub[value_col].dropna().astype(float)
        if len(s) < 2:
            continue
        m, se = s.mean(), s.sem()
        ci = stats.t.interval(0.95, len(s) - 1, loc=m, scale=se)
        rows.append({
            group_col: grp,
            'n': len(s),
            'mean': m,
            'median': s.median(),
            'std': s.std(),
            'ci_lower': ci[0],
            'ci_upper': ci[1],
        })
    return pd.DataFrame(rows).sort_values('mean', ascending=False)


def anova_oneway(df: pd.DataFrame, group_col: str, value_col: str) -> Dict[str, float]:
    groups = [g[value_col].dropna().astype(float).values for _, g in df.groupby(group_col)]
    groups = [g for g in groups if len(g) > 1]
    f_stat, p_val = stats.f_oneway(*groups)
    return {'f_stat': float(f_stat), 'p_value': float(p_val)}


def t_test(a: pd.Series, b: pd.Series, equal_var: bool = False) -> Dict[str, float]:
    a = a.dropna().astype(float)
    b = b.dropna().astype(float)
    t, p = stats.ttest_ind(a, b, equal_var=equal_var)
    return {'t_stat': float(t), 'p_value': float(p), 'mean_a': float(a.mean()), 'mean_b': float(b.mean())}


def detect_outliers_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    s = series.astype(float)
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    return (s < q1 - k * iqr) | (s > q3 + k * iqr)
