# 📖 Data Dictionary

This document catalogs every entity in the Housing Price & Geographic Analytics warehouse.

## fact_housing_listing

| Column | Type | Description |
|---|---|---|
| listing_id | BIGINT (PK) | Surrogate primary key |
| zip_id | INT (FK) | References dim_zip |
| property_type_id | INT (FK) | References dim_property_type |
| list_date_id | INT (FK) | References dim_date (listed) |
| sale_date_id | INT (FK) | References dim_date (sold) |
| list_price | NUMERIC(14,2) | Original list price (USD) |
| sale_price | NUMERIC(14,2) | Final sale price (USD) |
| bedrooms | SMALLINT | Number of bedrooms |
| bathrooms | NUMERIC(4,1) | Number of bathrooms |
| sqft_living | INT | Living area in sqft |
| sqft_lot | INT | Lot size in sqft |
| year_built | SMALLINT | Year built |
| hoa_fee_monthly | NUMERIC(8,2) | HOA fee per month |
| days_on_market | INT | DOM from list to sale |
| price_per_sqft | NUMERIC(10,2) | Derived: sale_price / sqft_living |
| latitude / longitude | NUMERIC(9,6) | WGS84 coordinates |
| geom | GEOMETRY(Point, 4326) | PostGIS geometry |

## fact_demographics

| Column | Type | Description |
|---|---|---|
| demo_id | BIGINT (PK) | Surrogate key |
| zip_id | INT (FK) | References dim_zip |
| date_id | INT (FK) | References dim_date |
| population | INT | Estimated population |
| median_age | NUMERIC(5,2) | Median age (years) |
| median_household_income | NUMERIC(12,2) | Median HH income (USD) |
| pct_bachelors_or_higher | NUMERIC(5,2) | % adults with BA+ degree |
| pct_owner_occupied | NUMERIC(5,2) | % owner-occupied housing |
| population_density | NUMERIC(10,2) | People per sq. mile |

## fact_economic_indicator

| Column | Type | Description |
|---|---|---|
| econ_id | BIGINT (PK) | Surrogate key |
| county_id | INT (FK) | References dim_county |
| date_id | INT (FK) | References dim_date |
| unemployment_rate | NUMERIC(5,2) | County unemployment rate |
| labor_force_participation | NUMERIC(5,2) | LFPR |
| gdp_per_capita | NUMERIC(14,2) | Local GDP per capita |
| mortgage_rate_30yr | NUMERIC(5,3) | 30-year fixed mortgage rate |
| consumer_price_index | NUMERIC(8,3) | CPI for the metro |
| months_supply | NUMERIC(5,2) | Inventory months of supply |
| new_construction_permits | INT | Permits issued in period |

## fact_neighborhood_score

| Column | Type | Description |
|---|---|---|
| score_id | BIGINT (PK) | Surrogate key |
| zip_id | INT (FK) | References dim_zip |
| date_id | INT (FK) | References dim_date |
| school_score | NUMERIC(4,1) | 1–10 school quality index |
| crime_index | NUMERIC(6,2) | Composite crime index |
| walk_score | NUMERIC(4,1) | Walk Score (0–100) |
| transit_score | NUMERIC(4,1) | Transit Score (0–100) |
| bike_score | NUMERIC(4,1) | Bike Score (0–100) |

## Dimension Tables

* **dim_state** — state codes, census region/division
* **dim_county** — county geometries (PostGIS MultiPolygon)
* **dim_zip** — ZIP centroid + county FK
* **dim_date** — calendar dimension (year, quarter, month, day_of_week)
* **dim_property_type** — Single Family, Condo, Townhouse, Multi-Family, Manufactured, Land

## Derived Features Used in Modeling

| Feature | Source | Notes |
|---|---|---|
| property_age | year_built | Current year - year_built |
| log_price | sale_price | log1p transform for normality |
| distance_to_cbd_km | lat/lon | Haversine to city center |
| price_zscore | sale_price | Z-score by ZIP |
| price_per_sqft | sale_price / sqft_living | Generated column |
