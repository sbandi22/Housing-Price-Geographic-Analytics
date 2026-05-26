"""Linear / OLS regression analysis (statsmodels)."""
import pandas as pd
import statsmodels.api as sm

from src.analytics.correlation import PRICE_DRIVERS


def fit_ols(df: pd.DataFrame, target: str = 'sale_price',
            features: list[str] | None = None) -> sm.regression.linear_model.RegressionResultsWrapper:
    features = features or [c for c in PRICE_DRIVERS
                            if c in df.columns and c != target]
    data = df[[target] + features].dropna()
    X = sm.add_constant(data[features].astype(float))
    y = data[target].astype(float)
    return sm.OLS(y, X).fit()


def summary_table(result) -> pd.DataFrame:
    return pd.DataFrame({
        'coef':   result.params,
        'std_err': result.bse,
        't':       result.tvalues,
        'p_value': result.pvalues,
        'ci_low':  result.conf_int()[0],
        'ci_high': result.conf_int()[1],
    })
