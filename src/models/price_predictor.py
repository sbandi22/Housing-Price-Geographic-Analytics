"""Housing price prediction model.

Trains a Gradient Boosting / XGBoost regressor and produces:
  * trained model artifact
  * RMSE / MAE / R\u00b2 metrics
  * feature importance chart
"""
import json
import logging
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.utils.config import MODEL, MODELS_DIR, REPORTS_DIR

log = logging.getLogger('predictor')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

NUM_FEATURES = [
    'sqft_living', 'sqft_lot', 'bedrooms', 'bathrooms', 'property_age',
    'hoa_fee_monthly', 'days_on_market',
    'median_household_income', 'unemployment_rate', 'population_density',
    'school_score', 'crime_index', 'walk_score',
    'mortgage_rate_30yr', 'months_supply',
]
CAT_FEATURES = ['property_type', 'state_code']
TARGET = 'sale_price'


def build_pipeline() -> Pipeline:
    pre = ColumnTransformer([
        ('num', StandardScaler(), NUM_FEATURES),
        ('cat', OneHotEncoder(handle_unknown='ignore'), CAT_FEATURES),
    ])
    reg = GradientBoostingRegressor(
        n_estimators=MODEL.n_estimators,
        max_depth=MODEL.max_depth // 2,
        learning_rate=MODEL.learning_rate,
        random_state=MODEL.random_state,
    )
    return Pipeline([('pre', pre), ('reg', reg)])


def train(df: pd.DataFrame) -> dict:
    df = df.dropna(subset=[TARGET])
    features = [c for c in NUM_FEATURES + CAT_FEATURES if c in df.columns]
    X = df[features].copy()
    y = df[TARGET].astype(float)

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=MODEL.test_size, random_state=MODEL.random_state
    )
    pipe = build_pipeline()
    pipe.fit(X_tr, y_tr)

    preds = pipe.predict(X_te)
    metrics = {
        'rmse': float(np.sqrt(mean_squared_error(y_te, preds))),
        'mae':  float(mean_absolute_error(y_te, preds)),
        'r2':   float(r2_score(y_te, preds)),
        'n_train': int(len(X_tr)),
        'n_test':  int(len(X_te)),
    }
    log.info('Metrics: %s', metrics)

    joblib.dump(pipe, MODELS_DIR / 'price_predictor.joblib')
    (MODELS_DIR / 'metrics.json').write_text(json.dumps(metrics, indent=2))
    _plot_feature_importance(pipe, features)
    return metrics


def _plot_feature_importance(pipe: Pipeline, feature_names: list[str]) -> Path:
    reg = pipe.named_steps['reg']
    pre = pipe.named_steps['pre']
    try:
        names = pre.get_feature_names_out()
    except Exception:
        names = feature_names
    imp = pd.Series(reg.feature_importances_, index=names).sort_values(ascending=True).tail(20)
    fig, ax = plt.subplots(figsize=(10, 8))
    imp.plot(kind='barh', ax=ax, color='steelblue')
    ax.set_title('Top 20 Feature Importances')
    ax.set_xlabel('Importance')
    fig.tight_layout()
    out = REPORTS_DIR / 'feature_importance.png'
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out


if __name__ == '__main__':
    sample = pd.read_csv('data/raw/sample_housing.csv')
    train(sample)
