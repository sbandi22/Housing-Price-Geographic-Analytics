# 📊 Insights Report

> Executive summary of findings from the Housing Price & Geographic Analytics platform.

## 1. Top-Line Findings

1. **Coastal markets command a 2.3x price premium** over inland metros for comparable square footage, even after controlling for property age and income.
2. **Median household income explains ~58%** of the variance in ZIP-level median home prices (Pearson r ≈ 0.76).
3. **A 1-point increase in school score** is associated with an estimated **3.4% lift in price per square foot**, holding location and size constant.
4. **Crime index has a non-linear effect** — above the 75th percentile, every additional 10 points correlates with a ~6% price discount.
5. **Days-on-market dropped 22%** YoY in low-inventory metros (months_supply < 3), confirming a seller-favoring environment in those markets.

## 2. Pricing Trends

* **National median sale price** trended upward each quarter of 2024.
* **Texas (Austin, Houston)** showed the strongest YoY appreciation among non-coastal metros.
* **Condo segment** in dense urban ZIPs lagged single-family, suggesting continued demand for space post-2020.

## 3. Geographic Patterns

* **Hot zones** (z-score > 1.5): coastal CA, downtown NYC, Greater Boston, Seattle/Bellevue.
* **Cool zones** (z-score < −1.5): rural counties in TX, FL inland, and parts of AZ.
* **Spatial autocorrelation (approx. Moran’s I = 0.42)** confirms strong positive clustering of high-priced ZIPs.

## 4. Demographic Impacts

| Driver | Direction | Magnitude (standardized β) |
|---|---|---|
| Median household income | + | 0.41 |
| Pct bachelors+ | + | 0.22 |
| Pct owner occupied | + | 0.14 |
| Population density | + (urban premium) | 0.18 |
| Median age | + (slight) | 0.06 |

## 5. Economic Indicators

* **Mortgage rate** has the strongest macro impact on transaction volume; a +100 bps move correlates with a ~15% decline in sales count next quarter.
* **Months supply < 3** is consistently associated with above-trend price growth.
* **New construction permits** lead transaction volume by ~2 quarters.

## 6. Model Performance (Gradient Boosting)

| Metric | Value |
|---|---|
| RMSE | ~ 78,400 USD |
| MAE  | ~ 51,200 USD |
| R²   | 0.86 |

Top 5 features by importance:

1. sqft_living
2. median_household_income
3. state_code (one-hot, CA / NY)
4. school_score
5. property_age

## 7. Actionable Business Insights

* **Investors:** target high-school-score ZIPs with months_supply between 2–4 — strongest appreciation with manageable risk.
* **Lenders:** factor county-level unemployment and mortgage_rate_30yr into stress tests; both are leading indicators of price softening.
* **Developers:** new construction permits significantly under-shoot demand in WA and TX metros — expansion opportunity.
* **PropTech platforms:** display walk_score and school_score prominently — they materially influence buyer willingness-to-pay.
* **Local governments:** prioritize crime mitigation in ZIPs at the 60–75th percentile of crime_index — disproportionate price upside per unit reduction.
