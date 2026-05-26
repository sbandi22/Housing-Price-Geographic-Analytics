-- ============================================================
-- Housing Price & Geographic Analytics : Normalized Schema (3NF)
-- Target DB: PostgreSQL 15 (with PostGIS extension)
-- ============================================================

CREATE EXTENSION IF NOT EXISTS postgis;

-- ---------- Dimension Tables ----------
CREATE TABLE IF NOT EXISTS dim_state (
    state_id        SERIAL PRIMARY KEY,
    state_code      CHAR(2) UNIQUE NOT NULL,
    state_name      VARCHAR(100) NOT NULL,
    census_region   VARCHAR(50),
    census_division VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dim_county (
    county_id   SERIAL PRIMARY KEY,
    state_id    INT NOT NULL REFERENCES dim_state(state_id) ON DELETE CASCADE,
    fips_code   VARCHAR(5) UNIQUE NOT NULL,
    county_name VARCHAR(150) NOT NULL,
    geom        GEOMETRY(MultiPolygon, 4326)
);

CREATE TABLE IF NOT EXISTS dim_zip (
    zip_id       SERIAL PRIMARY KEY,
    zip_code     VARCHAR(10) UNIQUE NOT NULL,
    county_id    INT REFERENCES dim_county(county_id),
    city         VARCHAR(150),
    latitude     NUMERIC(9,6),
    longitude    NUMERIC(9,6),
    geom         GEOMETRY(Point, 4326)
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id      INT PRIMARY KEY,        -- YYYYMMDD
    full_date    DATE NOT NULL UNIQUE,
    year         SMALLINT NOT NULL,
    quarter      SMALLINT NOT NULL,
    month        SMALLINT NOT NULL,
    month_name   VARCHAR(20),
    day          SMALLINT NOT NULL,
    day_of_week  SMALLINT NOT NULL,
    is_weekend   BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_property_type (
    property_type_id SERIAL PRIMARY KEY,
    type_name        VARCHAR(50) UNIQUE NOT NULL,
    description      TEXT
);

-- ---------- Fact Tables ----------
CREATE TABLE IF NOT EXISTS fact_housing_listing (
    listing_id        BIGSERIAL PRIMARY KEY,
    zip_id            INT NOT NULL REFERENCES dim_zip(zip_id),
    property_type_id  INT NOT NULL REFERENCES dim_property_type(property_type_id),
    list_date_id      INT REFERENCES dim_date(date_id),
    sale_date_id      INT REFERENCES dim_date(date_id),
    list_price        NUMERIC(14,2),
    sale_price        NUMERIC(14,2),
    bedrooms          SMALLINT,
    bathrooms         NUMERIC(4,1),
    sqft_living       INT,
    sqft_lot          INT,
    year_built        SMALLINT,
    hoa_fee_monthly   NUMERIC(8,2),
    days_on_market    INT,
    price_per_sqft    NUMERIC(10,2) GENERATED ALWAYS AS
        (CASE WHEN sqft_living > 0 THEN sale_price/sqft_living END) STORED,
    latitude          NUMERIC(9,6),
    longitude         NUMERIC(9,6),
    geom              GEOMETRY(Point, 4326)
);

CREATE INDEX IF NOT EXISTS idx_listing_geom ON fact_housing_listing USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_listing_zip  ON fact_housing_listing (zip_id);
CREATE INDEX IF NOT EXISTS idx_listing_sale_date ON fact_housing_listing (sale_date_id);

CREATE TABLE IF NOT EXISTS fact_demographics (
    demo_id                BIGSERIAL PRIMARY KEY,
    zip_id                 INT NOT NULL REFERENCES dim_zip(zip_id),
    date_id                INT NOT NULL REFERENCES dim_date(date_id),
    population             INT,
    median_age             NUMERIC(5,2),
    median_household_income NUMERIC(12,2),
    pct_bachelors_or_higher NUMERIC(5,2),
    pct_owner_occupied     NUMERIC(5,2),
    population_density     NUMERIC(10,2),
    UNIQUE (zip_id, date_id)
);

CREATE TABLE IF NOT EXISTS fact_economic_indicator (
    econ_id                  BIGSERIAL PRIMARY KEY,
    county_id                INT NOT NULL REFERENCES dim_county(county_id),
    date_id                  INT NOT NULL REFERENCES dim_date(date_id),
    unemployment_rate        NUMERIC(5,2),
    labor_force_participation NUMERIC(5,2),
    gdp_per_capita           NUMERIC(14,2),
    mortgage_rate_30yr       NUMERIC(5,3),
    consumer_price_index     NUMERIC(8,3),
    months_supply            NUMERIC(5,2),
    new_construction_permits INT,
    UNIQUE (county_id, date_id)
);

CREATE TABLE IF NOT EXISTS fact_neighborhood_score (
    score_id      BIGSERIAL PRIMARY KEY,
    zip_id        INT NOT NULL REFERENCES dim_zip(zip_id),
    date_id       INT NOT NULL REFERENCES dim_date(date_id),
    school_score  NUMERIC(4,1),
    crime_index   NUMERIC(6,2),
    walk_score    NUMERIC(4,1),
    transit_score NUMERIC(4,1),
    bike_score    NUMERIC(4,1),
    UNIQUE (zip_id, date_id)
);

-- ---------- Prediction Output ----------
CREATE TABLE IF NOT EXISTS model_predictions (
    prediction_id     BIGSERIAL PRIMARY KEY,
    listing_id        BIGINT REFERENCES fact_housing_listing(listing_id),
    model_version     VARCHAR(50) NOT NULL,
    predicted_price   NUMERIC(14,2) NOT NULL,
    prediction_error  NUMERIC(14,2),
    created_at        TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_pred_model ON model_predictions (model_version);
