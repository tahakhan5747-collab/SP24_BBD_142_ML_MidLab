"""Prediction-only backend. Train/export the three pipelines in the notebook."""

from pathlib import Path
from functools import lru_cache
import json
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(title="ML Lab: three predictions", version="3.0")
app.mount("/static", StaticFiles(directory=ROOT / "frontend"), name="static")


@lru_cache(maxsize=3)
def load_pipeline(name):
    """Load only trusted models exported by our notebook. Never train in a request."""
    path = ROOT / "models" / f"{name}_pipeline.joblib"
    if not path.exists():
        raise HTTPException(
            503,
            "Model missing. Run all cells in notebook/ML_Lab_Project.ipynb, then restart the server.",
        )
    return joblib.load(path)


class FuelInput(BaseModel):
    cylinders: int = Field(4, ge=3, le=8)
    displacement: float = Field(140, gt=0, le=600)
    horsepower: float = Field(90, gt=0, le=400)
    weight: float = Field(2500, ge=500, le=8000)
    acceleration: float = Field(16, gt=0, le=40)
    model_year: int = Field(76, ge=70, le=82)


class BankInput(BaseModel):
    age: int = Field(35, ge=18, le=100)
    balance: float = Field(1500, ge=-10000, le=1000000)
    campaign: int = Field(1, ge=1, le=100)
    pdays: int = Field(-1, ge=-1, le=1000)
    previous: int = Field(0, ge=0, le=100)
    threshold: float = Field(0.3, ge=0.01, le=0.99)


class SentimentInput(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


@app.get("/")
def index():
    return FileResponse(ROOT / "frontend/index.html")


@app.get("/api/status")
def status():
    return {
        "models": {
            name: (ROOT / "models" / f"{name}_pipeline.joblib").exists()
            for name in ["fuel", "bank", "sentiment"]
        }
    }


@app.get("/api/metadata")
def metadata():
    path = ROOT / "models/metadata.json"
    if not path.exists():
        raise HTTPException(503, "Metadata missing. Run the notebook export cell.")
    return json.loads(path.read_text(encoding="utf-8"))


@app.post("/api/predict/fuel")
def fuel(data: FuelInput):
    columns = [
        "cylinders",
        "displacement",
        "horsepower",
        "weight",
        "acceleration",
        "model_year",
    ]
    row = pd.DataFrame([data.model_dump()], columns=columns)
    prediction = float(load_pipeline("fuel").predict(row)[0])
    return {
        "predicted_mpg": prediction,
        "model": "Multiple linear regression",
        "note": "Estimate from historic Auto MPG data, not a modern-vehicle guarantee.",
    }


@app.post("/api/predict/bank")
def bank(data: BankInput):
    columns = ["age", "balance", "campaign", "pdays", "previous"]
    values = data.model_dump(exclude={"threshold"})
    probability = float(
        load_pipeline("bank").predict_proba(pd.DataFrame([values], columns=columns))[
            0, 1
        ]
    )
    return {
        "probability_subscribes": probability,
        "threshold": data.threshold,
        "predicted_class": (
            "Subscription" if probability >= data.threshold else "No subscription"
        ),
        "model": "Logistic regression: five numeric features",
        "note": "Lower thresholds may identify more subscribers while increasing unnecessary calls.",
    }


@app.post("/api/predict/sentiment")
def sentiment(data: SentimentInput):
    if not data.text.strip():
        raise HTTPException(422, "Enter a nonblank review.")
    probability = float(load_pipeline("sentiment").predict_proba([data.text])[0, 1])
    return {
        "probability_positive": probability,
        "predicted_class": "Positive" if probability >= 0.5 else "Negative",
        "model": "TF-IDF unigrams/bigrams + logistic regression",
        "note": "An estimate from a small English review dataset; human review is still useful.",
    }
