-- Analytical views for dashboards and reporting

CREATE OR REPLACE VIEW v_price_by_state_month AS
SELECT
    s.state_code,
    s.state_name,
    d.year,
    d.month,
    COUNT(*)                       AS sales_count,
    AVG(f.sale_price)::NUMERIC(14,2) AS avg_sale_price,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.sale_price)::NUMERIC(14,2) AS median_sale_price,
    AVG(f.price_per_sqft)::NUMERIC(10,2) AS avg_price_per_sqft
FROM fact_housing_listing f
JOIN dim_zip    z ON f.zip_id = z.zip_id
JOIN dim_county c ON z.county_id = c.county_id
JOIN dim_state  s ON c.state_id  = s.state_id
JOIN dim_date   d ON f.sale_date_id = d.date_id
WHERE f.sale_price IS NOT NULL
GROUP BY s.state_code, s.state_name, d.year, d.month;

CREATE OR REPLACE VIEW v_county_summary AS
SELECT
    c.county_id,
    c.county_name,
    s.state_code,
    COUNT(f.listing_id)                         AS total_sales,
    AVG(f.sale_price)::NUMERIC(14,2)            AS avg_sale_price,
    AVG(f.price_per_sqft)::NUMERIC(10,2)        AS avg_price_per_sqft,
    AVG(f.days_on_market)::NUMERIC(6,1)         AS avg_dom
FROM dim_county c
JOIN dim_state s ON c.state_id = s.state_id
LEFT JOIN dim_zip z              ON z.county_id = c.county_id
LEFT JOIN fact_housing_listing f ON f.zip_id    = z.zip_id
GROUP BY c.county_id, c.county_name, s.state_code;

CREATE OR REPLACE VIEW v_demographics_enriched AS
SELECT
    z.zip_code,
    s.state_code,
    d.year,
    fd.median_household_income,
    fd.population,
    fd.population_density,
    fd.pct_bachelors_or_higher,
    fd.pct_owner_occupied,
    fe.unemployment_rate,
    fe.mortgage_rate_30yr,
    ns.school_score,
    ns.crime_index,
    ns.walk_score
FROM fact_demographics fd
JOIN dim_zip      z ON fd.zip_id = z.zip_id
JOIN dim_county   c ON z.county_id = c.county_id
JOIN dim_state    s ON c.state_id = s.state_id
JOIN dim_date     d ON fd.date_id = d.date_id
LEFT JOIN fact_economic_indicator fe ON fe.county_id = c.county_id AND fe.date_id = fd.date_id
LEFT JOIN fact_neighborhood_score  ns ON ns.zip_id = z.zip_id    AND ns.date_id = fd.date_id;

CREATE OR REPLACE VIEW v_top_growing_zips AS
SELECT
    z.zip_code,
    s.state_code,
    AVG(CASE WHEN d.year = EXTRACT(YEAR FROM CURRENT_DATE) THEN f.sale_price END) AS price_current,
    AVG(CASE WHEN d.year = EXTRACT(YEAR FROM CURRENT_DATE) - 1 THEN f.sale_price END) AS price_prior,
    ROUND(
      (AVG(CASE WHEN d.year = EXTRACT(YEAR FROM CURRENT_DATE) THEN f.sale_price END)
       / NULLIF(AVG(CASE WHEN d.year = EXTRACT(YEAR FROM CURRENT_DATE)-1 THEN f.sale_price END),0) - 1) * 100,
      2
    ) AS yoy_pct
FROM fact_housing_listing f
JOIN dim_zip    z ON f.zip_id = z.zip_id
JOIN dim_county c ON z.county_id = c.county_id
JOIN dim_state  s ON c.state_id  = s.state_id
JOIN dim_date   d ON f.sale_date_id = d.date_id
GROUP BY z.zip_code, s.state_code;
