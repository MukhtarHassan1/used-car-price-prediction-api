"""FastAPI inference endpoints for the fitted regression pipeline."""
from fastapi import FastAPI
from app.inference import predict_price
from app.schema import CarFeatures, PredictionResponse

app = FastAPI(title="AutoValue AI — Used Car Price Prediction", version="2.0")


@app.get("/")
def root():
    return {"message": "AutoValue AI API", "docs": "/docs", "predict": "POST /predict"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: CarFeatures):
    price = predict_price(features.model_dump())
    return PredictionResponse(prediction_price=price)
