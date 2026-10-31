
# Used-Car Price Prediction — Reproducible Machine Learning & API

An end-to-end machine-learning project that estimates vehicle resale prices using structured car listing data. It covers **data validation, preprocessing, model training, evaluation against a baseline, reproducible inference, and API integration**.

The project uses a Scikit-Learn **Random Forest regressor**, a **FastAPI** prediction service, and an optional **Streamlit** interface. It is a portfolio experiment intended to show how a model can be developed, evaluated, tested, and served—not a production vehicle-pricing service.

## What the project does

- Prepares vehicle listing data and removes exact duplicate records before splitting.
- Encodes categorical features using a transformer fitted on the training data only.
- Trains a Random Forest model and compares it with a median-price baseline.
- Reports MAE, RMSE, and R² on a 20% holdout set.
- Saves the fitted preprocessing-and-model pipeline for consistent API predictions.
- Offers a documented `POST /predict` endpoint and a Streamlit front end.
- Includes automated tests, an experiment record, and a model card.

## Technology

**Python · Pandas · NumPy · Scikit-Learn · FastAPI · Pydantic · Streamlit · Pytest · Joblib**

## Dataset and features

The supplied `data/car_data.csv` contains **301 records** and nine columns. The target is `Selling_Price` measured in **Indian rupee lakhs** (1 lakh = ₹100,000).

| Input | Meaning |
| --- | --- |
| `Car_Name` | Vehicle name/model |
| `Year` | Vehicle model year (not sale timestamp) |
| `Present_Price` | Present/new vehicle price in INR lakhs |
| `Kms_Driven` | Distance driven in kilometers |
| `Fuel_Type` | Petrol, Diesel, or CNG |
| `Seller_Type` | Dealer or Individual |
| `Transmission` | Manual or Automatic |
| `Owner` | Previous-owner category |

**Dataset provenance:** The original repository did not document the dataset's authoritative download URL or redistribution license. Its structure resembles the widely used [CarDekho vehicle dataset on Kaggle](https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho), but that is not a verified attribution of these exact bytes. Confirm the source and applicable permissions before redistributing the CSV. Public availability alone does not establish redistribution permission.

## Evaluation results

Results reproduced locally from the supplied CSV using `python -m app.train`:

| Model | MAE (INR lakh) ↓ | RMSE (INR lakh) ↓ | R² ↑ |
| --- | ---: | ---: | ---: |
| **Random Forest (500 trees)** | **1.338492** | **3.198581** | **0.603041** |
| Median-price baseline | 3.347333 | 5.199533 | -0.048961 |

- **301** original rows; **2** exact duplicates removed before splitting.
- **239 training** rows and **60 holdout** rows (80/20 split, `random_state=42`).
- `OneHotEncoder(handle_unknown="ignore")` is fitted only on training data inside a Scikit-Learn pipeline.
- The baseline is fitted on the same training partition.
- No hyperparameters were tuned against the holdout set in this documented run.

These scores represent **one small random holdout experiment**, not a guarantee of accuracy on new listings. An MAE of 1.338492 INR lakh corresponds to approximately **₹133,849 average absolute error** on this test set.

See [Experiment & Reproducibility Notes](docs/EXPERIMENT.md), [Model Card](docs/MODEL_CARD.md), and the machine-readable [metrics](artifacts/metrics.json).

## Quick start

Tested for core training/API functionality with **Python 3.13.5**. Python 3.12+ is recommended.

### 1. Clone and set up

```bash
git clone https://github.com/MukhtarHassan1/used-car-price-prediction-api.git
cd used-car-price-prediction-api
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

Install the dependencies, including test tools:

```bash
python -m pip install -r requirements-dev.txt
```

If PowerShell blocks activation, you can run the environment's Python directly, for example:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

### 2. Retrain and evaluate

```bash
python -m app.train
```

This reads `data/car_data.csv` and generates:

- `artifacts/model.joblib` — the fitted preprocessor and Random Forest model.
- `artifacts/metrics.json` — metrics, split configuration, data SHA-256, and package versions.
- `artifacts/holdout_predictions.csv` — per-row holdout predictions and absolute errors.

The generated model file is excluded from Git because it is rebuildable and depends on the installed environment.

**Train before running the API.** Only load `.joblib` files you created or trust.

### 3. Run automated tests

```bash
python -m pytest -q
```

The current suite contains five tests covering:

- Dataset integrity and required features.
- Categorical encoding consistency.
- Training and evaluation artifacts.
- API predictions and input validation.
- Handling previously unseen vehicle categories.

Run training first so the saved-model-dependent tests execute rather than being skipped.

### 4. Start the prediction API

```bash
uvicorn app.api:app --reload
```

Available endpoints:

- Interactive API documentation: http://127.0.0.1:8000/docs
- Health endpoint: http://127.0.0.1:8000/health
- Prediction endpoint: `POST http://127.0.0.1:8000/predict`

Example request to `POST /predict`:

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

The response contains a numeric `prediction_price` and `unit: "INR lakh"`.

The prediction value depends on the trained model artifact. Invalid or missing inputs return HTTP 422.

### 5. Launch the Streamlit interface (optional)

Keep FastAPI running. In a second terminal, activate the same environment and run:

```bash
streamlit run app/ui.py
```

The interface sends prediction requests to `http://127.0.0.1:8000/predict` by default.

The endpoint can be overridden using the `CAR_PRICE_API_URL` environment variable (see `.env.example`).

The Streamlit source was reviewed, but the interface was not browser-tested during the reproducibility audit.

## How the model works

```text
CSV dataset
   |
   v
Validate required fields and remove exact duplicates
   |
   v
Train/test split (80/20, random_state=42)
   |
   v
Fit categorical OneHotEncoder on TRAIN ONLY
   |
   v
Train RandomForestRegressor (500 trees)
   |
   v
Evaluate on holdout and compare with median-price baseline
   |
   v
Save fitted preprocessing + model pipeline
   |
   v
Load the SAME pipeline for FastAPI predictions
```

### Training and inference consistency

The original prototype encoded a single prediction row using `pd.get_dummies(..., drop_first=True)`, which could discard categorical information.

The revised implementation uses one fitted `ColumnTransformer` inside a Scikit-Learn `Pipeline` for both training and inference.

The preprocessing transformation is learned from training data and then reused during prediction.

Unknown categories are handled without an encoding error, although prediction quality for unseen vehicle models has not been established.

## Repository structure

```text
app/
  __init__.py
  api.py                 FastAPI endpoints
  inference.py           Model loading and predictions
  pipeline.py            Shared features and sklearn pipeline
  schema.py              Input/output validation
  train.py               Training and evaluation
  ui.py                  Streamlit interface

artifacts/
  metrics.json           Evaluation metrics and metadata
  holdout_predictions.csv
  model.joblib           Generated locally; not tracked in Git

data/
  car_data.csv           Dataset (verify redistribution permissions)

docs/
  EXPERIMENT.md          Experimental design and reproducibility
  MODEL_CARD.md          Intended use, limitations and risks

tests/
  test_project.py        Automated regression checks

.env.example             Optional API URL setting
.gitignore
requirements.txt         Application dependencies
requirements-dev.txt     Application + test dependencies
CHANGELOG.md
README.md
```

## Reproducibility and limitations

**Repeatability:** The data checksum, random seed, model configuration, package versions, evaluation results, and holdout predictions are recorded. Retraining with the same data and compatible versions should reproduce the reported scores. The generated timestamp changes between runs.

**Small dataset:** Only 299 distinct records remain after removing duplicates. A single holdout evaluation is not enough to establish reliable performance across all vehicle categories.

**Dependence on original price:** `Present_Price` is required at prediction time. Its availability and reliability may limit the usefulness of the model.

**Unseen vehicles:** The pipeline can encode unknown vehicle names, but model accuracy on these inputs has not been established.

**Currency:** Target values and predictions are expressed in INR lakhs, not USD or PKR.

**Cross-sectional data:** The `Year` feature represents vehicle model year, not transaction time. This project does not implement chronological splitting, walk-forward validation, order-book forecasting, or trading backtests.

**Deployment:** This is an educational machine-learning and API engineering project, not a production valuation or financial decision system.

## Further improvements

Potential future work, not implemented in the current experiment:

- Repeated cross-validation and uncertainty reporting.
- Comparison with additional regression algorithms.
- Residual analysis by vehicle category and price range.
- Evaluation on a larger independent dataset.
- Containerized deployment and browser-level tests.

## Project context

This project was developed as a hands-on exercise in **machine-learning engineering, predictive modeling, Python APIs, and reproducible experimentation**.

The repository documents both the working implementation and its limitations so another developer can inspect the assumptions, rerun the experiments, verify the results, and build on the work.
