# Experiment and Reproducibility Notes

## Goal and dataset
Predict resale `Selling_Price` (in INR lakhs) from eight fields: `Car_Name`, `Year`, `Present_Price`, `Kms_Driven`, `Fuel_Type`, `Seller_Type`, `Transmission`, and `Owner`.

The supplied CSV has 301 rows and 9 columns, no null entries in the required columns, and 2 exact duplicates. Exact duplicates are removed before splitting. **The original source/license of the CSV was not documented in the submitted repository** and must be verified before redistributing.

## Protocol

1. Hash the original data file with SHA-256; retain its exact bytes.
2. Drop exact duplicate rows **before splitting**; keep all feature labels in their source form.
3. `train_test_split(test_size=0.2, shuffle=True, random_state=42)` on the remaining 299 records, giving 239 train / 60 test rows.
4. Fit `OneHotEncoder(handle_unknown='ignore')` **inside an sklearn Pipeline on the training fold only**. Numeric inputs pass through unchanged. The input target `Selling_Price` never enters the feature matrix.
5. Fit `RandomForestRegressor(n_estimators=500, random_state=42, n_jobs=1)`. No holdout-based hyperparameter tuning is performed.
6. Compare a median-target `DummyRegressor` fitted on the **same training partition**.
7. Report holdout **MAE, RMSE and R²** in `metrics.json`; save each held-out row, actual value, predicted value and absolute error in `holdout_predictions.csv`.
8. Persist the fitted **full Pipeline**, so the API uses the fitted encoder (not a second preprocessing implementation).

## Actual results (original supplied dataset)

| Model | MAE (INR lakh) | RMSE (INR lakh) | R² |
|---|---:|---:|---:|
| Random Forest | 1.338492 | 3.198581 | 0.603041 |
| Median baseline | 3.347333 | 5.199533 | -0.048961 |

See `artifacts/metrics.json` for exact environment versions and data checksum. These numbers are from **one random holdout** on a small dataset; report them as an experiment, not a statistically validated deployment result. RMSE is considerably larger than MAE, indicating some higher-error cases.

## Problems found during original source audit

- The repository README documented a completely unrelated FastAPI CRUD application.
- `train.py` expected `car-price-api/cardekho_data (1).csv` while the archive actually contained `car_data.csv` in a nested directory. It relied on a particular working directory and failed as provided.
- A **single-row categorical encoding bug**: calling `pd.get_dummies(..., drop_first=True)` during prediction can remove all categorical information from a single-row input. Training and inference used different effective feature representations.
- Dummy encoding ran on the entire dataset before the train/test split. The target was not encoded, but the category vocabulary was still learned using holdout records.
- The checked-in legacy pickled model was serialized with Scikit-Learn **1.5.1**, unlike the environment used in this audit (1.8.0); loading it displayed version-mismatch warnings. Regeneration is safer and reproducible.
- There was no saved holdout prediction table or metrics report for someone to inspect.
- Duplicate exact records were present. Removing them before splitting avoids one form of duplicate-record leakage.

## Failure modes still relevant

- Unknown vehicle names are supported but predictions for unseen makes/models are not validated here.
- No independent external dataset or repeated cross-validation study is included.
- The target is historical listing resale price; there is no prospective valuation test.
- `Present_Price` may correlate strongly with the target. In a real deployment, its availability and source need scrutiny.
- The `Year` variable is vehicle model year, **not a transaction timestamp**. This dataset cannot demonstrate walk-forward time-series evaluation or order-book leakage handling.
- The model does not carry fairness or safety guarantees; it is a technical demonstration only.

## Next experiments (not implemented / not claimed)

- Repeat splits or k-fold CV **on training data only** before final holdout evaluation; report uncertainty.
- Compare linear regression, gradient boosting and categorical treatments in a controlled way.
- Plot residuals grouped by vehicle category and price band to identify errors.
- Validate on an independently collected sample, with available prediction-time fields.
- For genuine market time-series work, collect timestamped events and use strictly chronological or embargoed validation, rather than reusing this random-split protocol.
