from fastapi.testclient import TestClient
from src.app.main import app, load_model

client = TestClient(app)


# 1. API contract test
def test_api_contract():
    health_resp = client.get("/health")
    assert health_resp.status_code == 200
    assert health_resp.json() == {"status": "healthy", "model_loaded": True}

    pred_resp = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert pred_resp.status_code == 200
    data = pred_resp.json()
    assert "prediction" in data
    assert "probabilities" in data
    assert isinstance(data["prediction"], int)
    assert isinstance(data["probabilities"], list)


# 2. Model loads test
def test_model_loads():
    loaded_model = load_model()
    assert loaded_model is not None
    assert hasattr(loaded_model, "predict")


# 3. Input schema validation test
def test_input_schema_validation():
    # Wrong length (only 2 features instead of 4)
    resp_short = client.post("/predict", json={"features": [5.1, 3.5]})
    assert resp_short.status_code == 422

    # Wrong data type (string instead of float)
    resp_type = client.post("/predict", json={"features": ["invalid", 3.5, 1.4, 0.2]})
    assert resp_type.status_code == 422


# 4. Edge case test
def test_edge_case_inputs():
    # Boundary zero values should return a valid prediction without crashing (no 500 error)
    resp_zeros = client.post("/predict", json={"features": [0.0, 0.0, 0.0, 0.0]})
    assert resp_zeros.status_code == 200

    # Extreme out-of-bounds value should be rejected cleanly with 422
    resp_extreme = client.post("/predict", json={"features": [1e9, 3.5, 1.4, 0.2]})
    assert resp_extreme.status_code == 422


# 5. Deterministic prediction test
def test_deterministic_prediction():
    payload = {"features": [6.3, 3.3, 6.0, 2.5]}
    first_response = client.post("/predict", json=payload).json()
    second_response = client.post("/predict", json=payload).json()
    assert first_response["prediction"] == second_response["prediction"]
    assert first_response["probabilities"] == second_response["probabilities"]