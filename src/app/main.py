import math
import os
from pathlib import Path
from typing import List

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

MODEL_PATH = Path(os.getenv("MODEL_PATH", "models/model.joblib"))

app = FastAPI(
    title="AI381 Lab 2 - ML Service",
    description="Containerized FastAPI ML model service with CI",
    version="1.0.0",
)


def load_model(path: Path = MODEL_PATH):
    if not path.exists():
        raise FileNotFoundError(f"Model file not found at {path}")
    return joblib.load(path)


model = load_model()


class PredictRequest(BaseModel):
    features: List[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="List of 4 numeric input features.",
    )

    @field_validator("features")
    @classmethod
    def validate_feature_values(cls, values: List[float]) -> List[float]:
        for val in values:
            if math.isnan(val) or math.isinf(val):
                raise ValueError("Features cannot contain NaN or infinite values.")
            if val < -1e6 or val > 1e6:
                raise ValueError("Feature values are out of acceptable bounds [-1e6, 1e6].")
        return values


class PredictResponse(BaseModel):
    prediction: int
    probabilities: List[float]


@app.get("/health")
def health_check():
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")
    return {"status": "healthy", "model_loaded": True}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    input_array = np.array(request.features, dtype=float).reshape(1, -1)
    pred = int(model.predict(input_array)[0])

    if hasattr(model, "predict_proba"):
        probs = [round(float(p), 4) for p in model.predict_proba(input_array)[0]]
    else:
        probs = [1.0]

    return PredictResponse(prediction=pred, probabilities=probs)