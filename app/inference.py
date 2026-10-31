"""Load the exact fitted preprocessing + model used for evaluation."""

from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

from app.pipeline import FEATURES

MODEL_PATH = Path(__file__).resolve().parents[1] / "artifacts" / "model.joblib"


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"Missing model artifact {MODEL_PATH}. Run: python -m app.train"
        )
    # Joblib uses pickle: only load models trained by you or trusted sources.
    return joblib.load(MODEL_PATH)


def predict_price(payload: dict) -> float:
    features = pd.DataFrame([payload], columns=FEATURES)
    return float(load_model().predict(features)[0])
