# Changes from supplied project ZIP

- Replaced an unrelated FastAPI CRUD README with verified ML project documentation.
- Simplified nested paths into a runnable project root (`app/`, `data/`, `artifacts/`, `tests/`).
- Fixed the missing CSV reference and working-directory-dependent training paths.
- Replaced inconsistent training/inference one-hot encoding with a fitted `ColumnTransformer` + `Pipeline`.
- Dropped exact duplicates *before* the train/test split; fitted preprocessing on training only.
- Added a fixed-seed 80/20 holdout evaluation with MAE, RMSE, R² and a median baseline.
- Generated exact holdout predictions, dataset checksum and environment metadata.
- Retrained the model from the included CSV; stopped depending on the incompatible old serialized model.
- Converted the API into a stable `app.api:app` module, with input validation and an explicit output unit.
- Kept the original Streamlit UI styling, making its API endpoint configurable.
- Added API, preprocessing and training tests; documented limitations, unverified UI behavior, and dataset license uncertainty.
