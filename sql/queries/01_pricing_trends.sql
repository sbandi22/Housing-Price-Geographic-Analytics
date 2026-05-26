-- Pricing trend analytical queries

-- 1. National price trend by quarter
SELECT d.year, d.quarter,
       COUNT(*) AS sales,
       AVG(f.sale_price)::NUMERIC(14,2) AS avg_price,
       AVG(f.price_per_sqft)::NUMERIC(10,2) AS avg_ppsf
FROM fact_housing_listing f
JOIN dim_date d ON f.sale_date_id = d.date_id
WHERE f.sale_price IS NOT NULL
GROUP BY d.year, d.quarter
ORDER BY d.year, d.quarter;

-- 2. YoY % change in median price by state
WITH yearly AS (
  SELECT s.state_code, d.year,
         PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.sale_price) AS median_price
  FROM fact_housing_listing f
  JOIN dim_zip z    ON f.zip_id = z.zip_id
  JOIN dim_county c ON z.county_id = c.county_id
  JOIN dim_state s  ON c.state_id  = s.state_id
  JOIN dim_date d   ON f.sale_date_id = d.date_id
  WHERE f.sale_price IS NOT NULL
  GROUP BY s.state_code, d.year
)
SELECT state_code, year, median_price,
       LAG(median_price) OVER (PARTITION BY state_code ORDER BY year) AS prior_year,
       ROUND(100*(median_price/NULLIF(LAG(median_price) OVER (PARTITION BY state_code ORDER BY year),0)-1),2) AS yoy_pct
FROM yearly;

-- 3. Price segmentation by property type
SELECT pt.type_name,
       COUNT(*) AS sales,
       AVG(f.sale_price)::NUMERIC(14,2)  AS avg_price,
       MIN(f.sale_price) AS min_price,
       MAX(f.sale_price) AS max_price,
       STDDEV(f.sale_price)::NUMERIC(14,2) AS std_price
FROM fact_housing_listing f
JOIN dim_property_type pt ON f.property_type_id = pt.property_type_id
GROUP BY pt.type_name
ORDER BY avg_price DESC;
