# 🚀 Deployment Guide

This guide explains how to deploy the Housing Price & Geographic Analytics platform locally and in production.

## 1. Prerequisites

- Python 3.10+
- PostgreSQL 15 with the **PostGIS** extension
- (Optional) Docker 24+ and Docker Compose v2
- Git

## 2. Local (no Docker)

```bash
git clone https://github.com/sbandi22/Housing-Price-Geographic-Analytics.git
cd Housing-Price-Geographic-Analytics

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # fill in DB credentials

psql -U postgres -c "CREATE DATABASE housing;"
psql -U postgres -d housing -f sql/schema.sql
psql -U postgres -d housing -f sql/seed.sql
psql -U postgres -d housing -f sql/views.sql

python -m src.etl.ingest
python -m src.etl.preprocess
python -m src.models.price_predictor
python dashboards/app.py
```

## 3. Docker (recommended)

```bash
docker-compose up -d --build
# Dashboard:  http://localhost:8050
# Postgres:   localhost:5432  (user: housing_admin)
```

Docker Compose will:

1. Spin up a **postgis/postgis:15-3.4** container
2. Bootstrap the schema, seed, and views automatically
3. Build and start the Python app container
4. Expose the Dash dashboard on **:8050**

## 4. Environment Variables

Create `.env` in the repository root:

```env
DB_HOST=postgres
DB_PORT=5432
DB_NAME=housing
DB_USER=housing_admin
DB_PASSWORD=housing_pass
```

## 5. Production Notes

- Run the dashboard behind **gunicorn** + **nginx** with HTTPS.
- Use **managed PostgreSQL** (e.g., RDS, Cloud SQL) with PostGIS enabled.
- Schedule the ETL via **Airflow**, **Prefect**, or a simple **cron** + Docker.
- Persist model artifacts to S3/GCS for reproducibility.

## 6. Troubleshooting

| Symptom | Fix |
|---|---|
| GeoPandas install fails | Ensure libgdal-dev, libgeos-dev, libproj-dev installed |
| PostGIS extension missing | `CREATE EXTENSION postgis;` as superuser |
| Dashboard 500 error | Check DB connectivity and that ETL has completed |
| Empty choropleth | Ensure `stg_us_states` geometries loaded |
