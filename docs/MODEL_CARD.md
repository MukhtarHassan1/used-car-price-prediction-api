# Model Card — AutoValue AI Random Forest

- **Purpose:** Educational estimate of historical vehicle resale price from structured listing inputs.
- **Model:** Scikit-Learn `RandomForestRegressor` inside a fitted `Pipeline` with `OneHotEncoder` for categorical features.
- **Source data:** Checked-in `data/car_data.csv`; 301 records before deduplication, 299 after. CSV provenance and redistribution rights were **not documented in the uploaded project**.
- **Target:** `Selling_Price` in Indian rupee lakhs (1 lakh = ₹100,000).
- **Inputs:** Year, original market price, kilometers driven, car name, fuel type, seller type, transmission, previous owner category.
- **Training/evaluation:** 239 training records; 60 random holdout test records; 42 seed; 500 trees; median baseline.
- **Performance on holdout:** MAE 1.338492 lakh; RMSE 3.198581 lakh; R² 0.603041. Baseline MAE 3.347333 lakh.
- **Intended users:** Students/reviewers inspecting an ML-to-API workflow.
- **Not intended for:** Live vehicle appraisals, credit/insurance decisions, trading, or price prediction with guaranteed accuracy.
- **Known weaknesses:** Small historical dataset, model/data drift, unknown categories, sensitivity to original market price, limited error analysis, no external validation.
- **Interpretation:** A prediction is an approximate point estimate, not a sale offer, confidence interval or calibrated uncertainty bound.
- **Reproducibility:** Run `python -m app.train`. See `docs/EXPERIMENT.md` and `artifacts/metrics.json`.
