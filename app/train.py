"""Train and evaluate from the checked-in CSV, saving reproducible artifacts."""

import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
import platform

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from app.pipeline import FEATURES, TARGET, make_pipeline

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "car_data.csv"
DEFAULT_ARTIFACTS = ROOT / "artifacts"


def get_data(path: Path):
    df = pd.read_csv(path)
    required = set(FEATURES + [TARGET])
    missing_columns = required.difference(df.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing_columns)}")
    # Avoid putting identical records on both sides of the split.
    n_before = len(df)
    df = df.drop_duplicates().copy()
    if df[FEATURES + [TARGET]].isna().any().any():
        raise ValueError("Missing data encountered; this experiment has no imputation strategy")
    if not np.isfinite(df[["Year", "Present_Price", "Kms_Driven", TARGET]].to_numpy(dtype=float)).all():
        raise ValueError("Non-finite numeric values encountered")
    return df, n_before - len(df)


def score(y_true, y_pred):
    return {
        "mae_lakhs": round(float(mean_absolute_error(y_true, y_pred)), 6),
        "rmse_lakhs": round(float(np.sqrt(mean_squared_error(y_true, y_pred))), 6),
        "r2": round(float(r2_score(y_true, y_pred)), 6),
    }


def run_experiment(data_path: Path = DEFAULT_DATA, artifacts_dir: Path = DEFAULT_ARTIFACTS, *, n_estimators: int = 500):
    data_path = Path(data_path)
    artifacts_dir = Path(artifacts_dir)
    df, removed_duplicates = get_data(data_path)
    if len(df) < 10:
        raise ValueError("Need at least 10 rows for this evaluation")

    X = df[FEATURES].copy()
    y = df[TARGET].copy()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, shuffle=True
    )

    # The train/test split happens BEFORE the encoding is fitted; test categories
    # cannot influence encoder vocabularies or the fitted regressor.
    model = make_pipeline(n_estimators=n_estimators, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    baseline = DummyRegressor(strategy="median")
    baseline.fit(X_train, y_train)
    baseline_predictions = baseline.predict(X_test)

    metrics = {
        "dataset": data_path.name,
        "dataset_sha256": hashlib.sha256(data_path.read_bytes()).hexdigest(),
        "original_rows": len(df) + removed_duplicates,
        "duplicate_rows_removed_before_split": removed_duplicates,
        "used_rows": len(df),
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "split": {"method": "random", "test_size": 0.20, "random_state": 42},
        "target": TARGET,
        "target_unit": "INR lakh (100,000 rupees)",
        "features": FEATURES,
        "model": "RandomForestRegressor",
        "n_estimators": n_estimators,
        "model_metrics": score(y_test, predictions),
        "median_baseline_metrics": score(y_test, baseline_predictions),
        "python_version": platform.python_version(),
        "scikit_learn_version": sklearn.__version__,
        "pandas_version": pd.__version__,
        "numpy_version": np.__version__,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "evaluation_warning": "Random holdout on historical cross-sectional data; NOT a walk-forward or trading strategy backtest",
    }

    holdout = X_test.copy()
    holdout.insert(0, "source_row_index", X_test.index)
    holdout["actual_selling_price_lakhs"] = y_test.to_numpy()
    holdout["predicted_selling_price_lakhs"] = predictions
    holdout["absolute_error_lakhs"] = abs(predictions - y_test.to_numpy())
    holdout = holdout.sort_values("source_row_index")

    artifacts_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, artifacts_dir / "model.joblib")
    (artifacts_dir / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    holdout.to_csv(artifacts_dir / "holdout_predictions.csv", index=False)
    return metrics


def main():
    p = argparse.ArgumentParser(description="Train, score, and export car price regression artifacts")
    p.add_argument("--data", type=Path, default=DEFAULT_DATA)
    p.add_argument("--artifacts", type=Path, default=DEFAULT_ARTIFACTS)
    p.add_argument("--n-estimators", type=int, default=500)
    args = p.parse_args()
    if args.n_estimators < 1:
        p.error("--n-estimators must be >= 1")
    print(json.dumps(run_experiment(args.data, args.artifacts, n_estimators=args.n_estimators), indent=2))


if __name__ == "__main__":
    main()
