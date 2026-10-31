"""Regression checks for data integrity, encoder consistency, CLI artifacts, and API."""

from pathlib import Path

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from app.api import app
from app.inference import MODEL_PATH, load_model, predict_price
from app.pipeline import CATEGORICAL_FEATURES, FEATURES, TARGET, make_pipeline
from app.train import DEFAULT_DATA, get_data, run_experiment


SAMPLE = {
    "Car_Name": "swift",
    "Year": 2014,
    "Present_Price": 6.87,
    "Kms_Driven": 42450,
    "Fuel_Type": "Diesel",
    "Seller_Type": "Dealer",
    "Transmission": "Manual",
    "Owner": 0,
}


def test_dataset_has_expected_features_no_nulls_or_target_in_features():
    df, duplicates = get_data(DEFAULT_DATA)
    assert len(df) > 250
    assert duplicates == 2
    assert TARGET not in FEATURES
    assert all(column in df.columns for column in FEATURES + [TARGET])
    assert not df.isna().any().any()


def test_encoder_keeps_all_categorical_features_even_for_one_prediction():
    df, _ = get_data(DEFAULT_DATA)
    model = make_pipeline(n_estimators=5)
    model.fit(df[FEATURES], df[TARGET])
    frame1 = pd.DataFrame([SAMPLE], columns=FEATURES)
    frame2 = frame1.copy()
    frame2["Fuel_Type"] = "Petrol"
    frame3 = frame1.copy()
    frame3["Car_Name"] = "ciaz"
    prep = model.named_steps["preprocessor"]
    assert prep.transform(frame1).shape == prep.transform(frame2).shape
    assert (prep.transform(frame1) != prep.transform(frame2)).any(), "Fuel type must not disappear at inference"
    assert (prep.transform(frame1) != prep.transform(frame3)).any(), "Car name must not disappear at inference"
    assert set(CATEGORICAL_FEATURES).issubset(frame1.columns)


def test_training_writes_metrics_and_predictions(tmp_path):
    result = run_experiment(DEFAULT_DATA, tmp_path, n_estimators=10)
    assert (tmp_path / "model.joblib").is_file()
    assert (tmp_path / "metrics.json").is_file()
    pred = pd.read_csv(tmp_path / "holdout_predictions.csv")
    assert len(pred) == result["test_rows"]
    assert result["train_rows"] + result["test_rows"] == result["used_rows"]
    assert result["model_metrics"]["mae_lakhs"] >= 0
    assert result["split"]["random_state"] == 42


@pytest.mark.skipif(not MODEL_PATH.is_file(), reason="Train the model with python -m app.train first")
def test_saved_model_matches_api():
    assert load_model() is load_model()
    price = predict_price(SAMPLE)
    assert 0 < price < 100
    with TestClient(app) as client:
        response = client.post("/predict", json=SAMPLE)
        assert response.status_code == 200, response.text
        assert response.json()["prediction_price"] == pytest.approx(price)
        assert response.json()["unit"] == "INR lakh"
        assert client.get("/health").json() == {"status": "ok"}
        invalid = client.post("/predict", json={**SAMPLE, "Kms_Driven": -1})
        assert invalid.status_code == 422
        missing = client.post("/predict", json={"Year": 2014})
        assert missing.status_code == 422


@pytest.mark.skipif(not MODEL_PATH.is_file(), reason="Train the model with python -m app.train first")
def test_unknown_category_is_handled():
    unknown_car = dict(SAMPLE, Car_Name="unseen-demo-model")
    prediction = predict_price(unknown_car)
    assert prediction > 0
