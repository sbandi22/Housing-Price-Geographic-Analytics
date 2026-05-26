# 🏘️ Housing Price & Geographic Analytics

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)
![Tableau](https://img.shields.io/badge/Tableau-Style-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

> **End-to-end data analytics platform** for analyzing housing prices, geographic patterns, economic indicators, and demographic impacts. Built with Python, SQL, PostgreSQL, Pandas, Plotly, GeoPandas, and a Tableau-style interactive dashboard.

---

## 📌 Project Overview

The **Housing Price & Geographic Analytics** project is a production-grade analytics platform engineered by a senior data analyst & data engineer. It ingests multi-source housing and demographic data, normalizes it into a relational warehouse, performs geospatial and statistical analysis, and surfaces insights via interactive dashboards and automated reports.

### 🎯 Objectives

- Identify **pricing trends** across regions and time
- Reveal **geographic patterns** via choropleth heatmaps
- Quantify **economic indicators** that move home prices
- Measure **demographic impacts** on housing affordability
- Deliver **price predictions** with feature importance

---

## 🧩 Core Features

| # | Feature | Module |
|---|---------|--------|
| 1 | Data ingestion pipeline | `src/etl/ingest.py` |
| 2 | SQL database design (3NF) | `sql/schema.sql` |
| 3 | Geographic trend analysis | `src/analytics/geo_analysis.py` |
| 4 | Statistical analysis | `src/analytics/stats.py` |
| 5 | Correlation analysis | `src/analytics/correlation.py` |
| 6 | Tableau-style dashboard | `dashboards/app.py` |
| 7 | Regional heatmaps (choropleth) | `src/analytics/heatmap.py` |
| 8 | Housing price prediction (ML) | `src/models/price_predictor.py` |
| 9 | Data cleaning & normalization | `src/etl/preprocess.py` |
| 10 | Automated reporting | `src/reports/report_generator.py` |

---

## 🏗️ Architecture

```
┌────────────┐    ┌─────────────┐    ┌──────────────┐    ┌───────────────┐
│  Raw CSVs  │───▶│  ETL Layer  │───▶│  PostgreSQL  │───▶│  Analytics &  │
│  APIs/Geo  │    │  (Pandas)   │    │   (3NF DW)   │    │  ML Modeling  │
└────────────┘    └─────────────┘    └──────────────┘    └───────┬───────┘
                                                                 │
                                                                 ▼
                                                  ┌──────────────────────────┐
                                                  │ Dashboard + Reports +    │
                                                  │ Choropleth Heatmaps      │
                                                  └──────────────────────────┘
```

---

## 📂 Folder Structure

```
Housing-Price-Geographic-Analytics/
├── data/
│   ├── raw/                 # Original CSV / GeoJSON files
│   ├── interim/             # Cleaned intermediate data
│   ├── processed/           # Final modeling-ready datasets
│   └── external/            # Census, economic, geo lookups
├── sql/
│   ├── schema.sql           # Normalized 3NF schema
│   ├── seed.sql             # Reference / lookup seeds
│   ├── views.sql            # Analytical views
│   └── queries/             # Reusable analytical queries
├── src/
│   ├── etl/                 # Ingestion + preprocessing
│   ├── analytics/           # Stats, correlation, geo analytics
│   ├── models/              # ML: regression + feature importance
│   ├── reports/             # Automated reporting
│   └── utils/               # Helpers, config, DB connection
├── notebooks/               # Jupyter EDA & modeling notebooks
├── dashboards/              # Tableau-style Plotly/Dash app
├── reports/                 # Generated HTML/PDF insight reports
├── docker/                  # Dockerfile + compose service files
├── tests/                   # Pytest unit & integration tests
├── screenshots/             # Dashboard & heatmap screenshots
├── docs/                    # Data dictionary, insights, deployment
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🛠️ Tech Stack

- **Languages:** Python 3.10+, SQL
- **Database:** PostgreSQL 15 (with PostGIS) / MySQL compatible
- **Data:** Pandas, NumPy, GeoPandas, Shapely
- **Modeling:** scikit-learn, statsmodels, XGBoost
- **Visualization:** Plotly, Dash, Folium, Matplotlib, Seaborn
- **Orchestration:** Make + Docker Compose
- **Notebooks:** Jupyter

---

## 📊 15+ Pricing Trend Factors

1. Median household income
2. Population density
3. Unemployment rate
4. School quality index
5. Crime rate index
6. Median age of population
7. Property tax rate
8. Distance to CBD (city center)
9. Number of bedrooms / bathrooms
10. Square footage (living area)
11. Lot size
12. Year built / property age
13. HOA fees
14. Walk Score / Transit Score
15. Mortgage interest rate (macro)
16. Inventory months of supply
17. Days on market
18. Price per square foot (regional)
19. New construction permits
20. Migration / net inflow rate

---

## 🗺️ Geographic Analytics

- **Choropleth maps** by state / county / ZIP
- **Hotspot detection** (Getis-Ord Gi*)
- **Spatial autocorrelation** (Moran's I)
- **Distance-to-amenity** features (PostGIS `ST_Distance`)

---

## 🤖 Machine Learning

- Baseline: **Linear / Ridge / Lasso regression**
- Tree-based: **Random Forest, Gradient Boosting, XGBoost**
- Evaluation: RMSE, MAE, R²
- Explainability: **feature importance + SHAP**

---

## 🚀 Quickstart

```bash
# 1. Clone
git clone https://github.com/sbandi22/Housing-Price-Geographic-Analytics.git
cd Housing-Price-Geographic-Analytics

# 2. Spin up Postgres + app via Docker
docker-compose up -d

# 3. Or run locally
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 4. Initialize the database
psql -U postgres -d housing -f sql/schema.sql
psql -U postgres -d housing -f sql/seed.sql

# 5. Run ETL
python -m src.etl.ingest
python -m src.etl.preprocess

# 6. Train model
python -m src.models.price_predictor

# 7. Launch dashboard
python dashboards/app.py     # http://localhost:8050
```

---

## 📸 Screenshots

> Place exported PNGs under `screenshots/`.

| Dashboard Overview | Choropleth Heatmap |
|--------------------|--------------------|
| ![Dashboard](screenshots/dashboard_overview.png) | ![Heatmap](screenshots/choropleth_heatmap.png) |

| Correlation Matrix | Feature Importance |
|--------------------|--------------------|
| ![Correlation](screenshots/correlation_matrix.png) | ![Feature Importance](screenshots/feature_importance.png) |

---

## 📚 Documentation

- [Data Dictionary](docs/DATA_DICTIONARY.md)
- [Insights Report](docs/INSIGHTS_REPORT.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

---

## 🧪 Testing

```bash
pytest tests/ -v --cov=src
```

---

## 📄 License

MIT © 2026 sbandi22
