-- Reference seeds for the housing analytics warehouse

INSERT INTO dim_property_type (type_name, description) VALUES
  ('Single Family',     'Detached single-family home'),
  ('Condo',             'Condominium unit'),
  ('Townhouse',         'Attached townhouse'),
  ('Multi-Family',      '2-4 unit residential property'),
  ('Manufactured',      'Manufactured / mobile home'),
  ('Land',              'Vacant land parcel')
ON CONFLICT (type_name) DO NOTHING;

INSERT INTO dim_state (state_code, state_name, census_region, census_division) VALUES
  ('CA', 'California',     'West',      'Pacific'),
  ('TX', 'Texas',          'South',     'West South Central'),
  ('NY', 'New York',       'Northeast', 'Middle Atlantic'),
  ('FL', 'Florida',        'South',     'South Atlantic'),
  ('WA', 'Washington',     'West',      'Pacific'),
  ('IL', 'Illinois',       'Midwest',   'East North Central'),
  ('CO', 'Colorado',       'West',      'Mountain'),
  ('GA', 'Georgia',        'South',     'South Atlantic'),
  ('MA', 'Massachusetts',  'Northeast', 'New England'),
  ('AZ', 'Arizona',        'West',      'Mountain')
ON CONFLICT (state_code) DO NOTHING;

-- Populate dim_date with last 6 years (helper: run from Python ETL ideally)
INSERT INTO dim_date (date_id, full_date, year, quarter, month, month_name, day, day_of_week, is_weekend)
SELECT
  TO_CHAR(d, 'YYYYMMDD')::INT,
  d::DATE,
  EXTRACT(YEAR FROM d)::SMALLINT,
  EXTRACT(QUARTER FROM d)::SMALLINT,
  EXTRACT(MONTH FROM d)::SMALLINT,
  TO_CHAR(d, 'Month'),
  EXTRACT(DAY FROM d)::SMALLINT,
  EXTRACT(ISODOW FROM d)::SMALLINT,
  EXTRACT(ISODOW FROM d) IN (6,7)
FROM generate_series('2020-01-01'::DATE, '2026-12-31'::DATE, '1 day') d
ON CONFLICT (date_id) DO NOTHING;
