import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_current_gold_price():
    client = TestClient(app)
    response = client.get("/current")
    assert response.status_code == 200
    data = response.json()
    assert "price_bhd_per_gram" in data
    assert data["currency"] == "BHD"
    assert data["unit"] == "gram"
    assert data["carat"] == 24

def test_historical_gold_price():
    client = TestClient(app)
    response = client.get("/history?date=20230101")
    assert response.status_code == 200
    data = response.json()
    assert "date" in data
    assert data["date"] == "20230101"
    assert "price_bhd_per_gram" in data
    assert data["currency"] == "BHD"
    assert data["unit"] == "gram"
    assert data["carat"] == 24

def test_convert_gold_to_currency():
    client = TestClient(app)
    response = client.get("/convert?amount_grams=10")
    assert response.status_code == 200
    data = response.json()
    assert "amount_grams" in data
    assert data["amount_grams"] == 10
    assert "total_value" in data
    assert "currency" in data
    assert data["currency"] == "BHD"

def test_invalid_date_format():
    client = TestClient(app)
    response = client.get("/history?date=2023-01-01")
    assert response.status_code == 422  # Unprocessable Entity due to regex validation

def test_missing_date_parameter():
    client = TestClient(app)
    response = client.get("/history")
    assert response.status_code == 422  # Unprocessable Entity due to missing required parameter

def test_negative_amount_grams():
    client = TestClient(app)
    response = client.get("/convert?amount_grams=-5")
    assert response.status_code == 400  # Unprocessable Entity due to negative value

