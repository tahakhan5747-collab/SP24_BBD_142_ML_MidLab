"""Prediction-only integration checks. Run with the project environment."""

from pathlib import Path
import importlib.util
import json
import math
import tempfile

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "prediction_backend", ROOT / "backend/main.py"
)
backend = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend)

with TestClient(backend.app) as client:
    assert client.get("/").status_code == 200
    for name in ["app.js", "style.css"]:
        assert client.get("/static/" + name).status_code == 200
    status = client.get("/api/status").json()
    assert all(status["models"].values()), status
    metadata = client.get("/api/metadata")
    assert metadata.status_code == 200

    fuel_input = dict(
        cylinders=4,
        displacement=140,
        horsepower=90,
        weight=2500,
        acceleration=16,
        model_year=76,
    )
    fuel = client.post("/api/predict/fuel", json=fuel_input)
    assert fuel.status_code == 200, fuel.text
    assert math.isfinite(fuel.json()["predicted_mpg"])

    bank_input = dict(
        age=35, balance=1500, campaign=1, pdays=-1, previous=0, threshold=0.3
    )
    bank = client.post("/api/predict/bank", json=bank_input)
    assert bank.status_code == 200, bank.text
    probability = bank.json()["probability_subscribes"]
    assert 0 <= probability <= 1
    assert bank.json()["predicted_class"] == (
        "Subscription" if probability >= 0.3 else "No subscription"
    )

    for review in [
        "The food was delicious and the service was friendly.",
        "The food was cold and the service was rude.",
    ]:
        result = client.post("/api/predict/sentiment", json={"text": review})
        assert result.status_code == 200, result.text
        assert 0 <= result.json()["probability_positive"] <= 1
    assert (
        client.post("/api/predict/sentiment", json={"text": "   "}).status_code == 422
    )
    assert (
        client.post(
            "/api/predict/bank", json={**bank_input, "threshold": 2}
        ).status_code
        == 422
    )
    assert (
        client.post("/api/predict/fuel", json={**fuel_input, "weight": -1}).status_code
        == 422
    )

    # Missing files should produce a useful message, not prevent the app importing.
    original_root = backend.ROOT
    backend.load_pipeline.cache_clear()
    try:
        with tempfile.TemporaryDirectory() as directory:
            backend.ROOT = Path(directory)
            missing = client.post("/api/predict/fuel", json=fuel_input)
            assert missing.status_code == 503
            assert "Run all cells" in missing.json()["detail"]
    finally:
        backend.ROOT = original_root
        backend.load_pipeline.cache_clear()

notebook = json.loads((ROOT / "notebook/ML_Lab_Project.ipynb").read_text())
code = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
assert len(code) == 21
assert all(cell.get("execution_count") is not None for cell in code)
assert not any(
    "from backend" in "".join(cell["source"]) or "import backend" in "".join(cell["source"])
    for cell in code
)
for cell in code:
    assert not any(
        output.get("output_type") == "error" for output in cell.get("outputs", [])
    )
results = json.loads((ROOT / "results/notebook_results.json").read_text())
assert len(results["regression"]) == 6
assert len(results["trees"]) == 4 and len(results["ensembles"]) == 5
assert len(results["svm_nb"]) == 6 and len(results["svm_sensitivity"]) == 4
assert len(results["imbalance"]) == 6 and len(results["text_models"]) == 10
print(
    "Passed: three predictions, validation errors, missing-model behavior, static files,"
)
print("self-contained executed notebook and full activity coverage.")
print("Example fuel prediction:", fuel.json()["predicted_mpg"])
print("Example subscription probability:", probability)
