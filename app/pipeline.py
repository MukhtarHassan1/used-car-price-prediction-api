"""Shared feature schema and fitted preprocessing for training and inference."""

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

TARGET = "Selling_Price"
NUMERIC_FEATURES = ["Year", "Present_Price", "Kms_Driven"]
CATEGORICAL_FEATURES = ["Car_Name", "Fuel_Type", "Seller_Type", "Transmission", "Owner"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def make_pipeline(*, n_estimators: int = 500, random_state: int = 42) -> Pipeline:
    """Fit one encoding pipeline on the training fold, then reuse it for prediction.

    Unknown categories (including unseen car names) are encoded as all zeroes
    for their category group. This is a fallback, not a claim of model quality
    on unseen vehicle models.
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
            ("numeric", "passthrough", NUMERIC_FEATURES),
        ],
        remainder="drop",
    )
    return Pipeline([
        ("preprocessor", preprocessor),
        ("model", RandomForestRegressor(n_estimators=n_estimators, random_state=random_state, n_jobs=1)),
    ])
