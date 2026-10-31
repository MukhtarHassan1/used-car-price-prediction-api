# AutoValue AI — Reproducible Used-Car Price Prediction

A small **end-to-end regression project**, from a checked-in CSV to a fitted Random Forest model, a reproducible holdout evaluation, a FastAPI inference endpoint, and an optional Streamlit UI.

This is a learning/portfolio experiment on **cross-sectional car resale listings**. It is **not** a financial time-series forecasting system, a trading model, or a production valuation service.

## Results from the supplied data

Reproduced locally using the included `data/car_data.csv` and `python -m app.train`:

| Model | Holdout MAE (INR lakh) ↓ | Holdout RMSE (INR lakh) ↓ | R² ↑ |
| --- | ---: | ---: | ---: |
| Random Forest, 500 trees | **1.338492** | **3.198581** | **0.603041** |
| Median-price baseline | 3.347333 | 5.199533 | -0.048961 |

- Original CSV: **301 records**; **2 exact duplicate records** removed before splitting.
- After deduplication: **239 training / 60 test records** (80/20 shuffled holdout, `random_state=42`).
- The unit is an **Indian lakh of rupees (₹100,000)**, **not dollars or Pakistani rupees**.
- This is one relatively small random holdout; these numbers are **not guaranteed generalization performance**. See [experiment notes](docs/EXPERIMENT.md) and [model card](docs/MODEL_CARD.md).

## Quick start (Windows, macOS or Linux)

**Requires Python 3.12+** (the core training/API/tests were exercised with Python 3.13.5). Commands below work in a terminal from the project root.

```bash
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Then install dependencies and **train from source**:

```bash
python -m pip install -r requirements-dev.txt
python -m app.train
python -m pytest -q
```

Training produces:

- `artifacts/model.joblib` — fitted **preprocessing + model pipeline**, not just a bare regressor.
- `artifacts/metrics.json` — experiment configuration, dataset checksum, versions and evaluation scores.
- `artifacts/holdout_predictions.csv` — each held-out record and its actual/predicted price and absolute error.

> `artifacts/model.joblib` is gitignored because generated binary models are environment/version-dependent. **Anyone cloning the repository can regenerate it by running `python -m app.train`.** Only load `.joblib` artifacts you created or trust: they are pickle-based files.

### Run the prediction API

Start FastAPI in terminal 1:

```bash
uvicorn app.api:app --reload
```

Browse [interactive API docs](http://127.0.0.1:8000/docs), then try **POST /predict** with:

```json
{
  "Car_Name": "swift",
  "Year": 2014,
  "Present_Price": 6.87,
  "Kms_Driven": 42450,
  "Fuel_Type": "Diesel",
  "Seller_Type": "Dealer",
  "Transmission": "Manual",
  "Owner": 0
}
```

The API returns `prediction_price` and `unit: "INR lakh"` (e.g. a value of `4.6` would mean ₹460,000). Input validation errors return HTTP 422.

### Run the Streamlit interface (optional)

With the API running in terminal 1, use terminal 2 (same environment):

```bash
streamlit run app/ui.py
```

The UI calls `http://127.0.0.1:8000/predict` by default. Override the endpoint through the optional `CAR_PRICE_API_URL` environment variable. Streamlit wasn't installed in the audit environment, so **the UI was code-reviewed but not browser-tested** as part of the reproducibility verification.

## How the experiment is structured

```text
data/car_data.csv
    → remove exact duplicate rows
    → train/test split (80/20, seed 42)
    → fit OneHotEncoder on TRAIN ONLY; ignore unseen categories at inference
    → train RandomForestRegressor (500 trees, seed 42)
    → evaluate held-out data against median-price baseline
    → write trained Pipeline + metrics + held-out predictions
    → API loads that same fitted Pipeline for single-record inference
```

**Why this matters:** The original code used `pd.get_dummies(drop_first=True)` on a single input row at inference time, so categorical information was lost. The fixed implementation fits a `ColumnTransformer` and `OneHotEncoder` on training data and uses the **same transformer** during inference. Training no longer depends on the current terminal's working directory.

## Files

```text
app/
  pipeline.py          Training/inference feature schema and sklearn pipeline
  train.py             Training, baseline comparison and holdout exports
  inference.py         Load the fitted pipeline, perform inference
  schema.py            Pydantic request/response validation
  api.py               FastAPI REST API
  ui.py                Streamlit front end (original design retained)
data/car_data.csv      Original supplied dataset
artifacts/             metrics.json, holdout_predictions.csv; generated model is gitignored
docs/EXPERIMENT.md     Experimental design, bugs found, repeatability
docs/MODEL_CARD.md    Dataset limitations, intended use and risks
tests/test_project.py Automated checks for preprocessing, training and API
requirements.txt      Application dependencies
requirements-dev.txt  App + testing dependencies
```

## Limitations and interpretation

1. There are only 299 distinct rows; a single holdout estimate can be noisy. The data contains a mix of cars and two-wheelers.
2. Car names are categorical. Unseen names will be encoded as unknown (no category flag); this prevents a crash but **does not guarantee a meaningful price**.
3. `Present_Price` is provided at prediction time. A user may not know this value, and it can dominate the prediction. It is not the target `Selling_Price`, but the reliance on this input limits practical utility.
4. These are **cross-sectional records**, not chronological trades. A random holdout is *not* valid evidence of financial forecasting accuracy. For financial time series, use chronological/walk-forward validation with leakage controls.
5. The original ZIP did not contain a trustworthy source/license notice for the dataset. **Verify its origin and reuse rights before redistributing or publishing the CSV.** If you can't confirm permission, replace it with appropriately licensed data and rerun the experiment.

## Re-running and checking results

Run `python -m app.train` again with the same dataset and pinned core dependencies. The **scores and per-record predictions** should match. The `created_utc` field in `metrics.json` will change by design. To verify dataset identity, compare the `dataset_sha256` field.

For code verification, run `python -m pytest -q`; tests check feature correctness, categorical encoding, model training artifacts, API response shape and input validation.

---

Built as a learning project in Python, Scikit-Learn, Pandas, FastAPI and Streamlit. The original interface design is preserved; the model-training pipeline and documentation have been refactored for reproducibility and correct inference.
