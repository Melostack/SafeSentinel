import os
from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)

def test_missing_auth():
    response = client.post("/extract", json={"text": "test"})
    assert response.status_code == 401

    response = client.post("/check", json={
        "asset": "USDT", "origin": "Binance", "destination": "OKX",
        "network": "TRC20", "address": "T123456789012345678901234567890123"
    })
    assert response.status_code == 401
    print("Missing auth tests passed.")

def test_valid_auth():
    os.environ["SAFE_SENTINEL_API_KEY"] = "super-secret"
    headers = {"X-API-Key": "super-secret"}
    # The humanizer mock should return 400 since it is a mock intent extractor
    # we just care it doesn't return 401
    response = client.post("/extract", json={"text": "test"}, headers=headers)
    assert response.status_code != 401

    response = client.post("/check", json={
        "asset": "USDT", "origin": "Binance", "destination": "OKX",
        "network": "TRC20", "address": "T123456789012345678901234567890123"
    }, headers=headers)
    assert response.status_code != 401
    print("Valid auth tests passed.")

if __name__ == "__main__":
    os.environ["SAFE_SENTINEL_API_KEY"] = "super-secret"
    test_missing_auth()
    test_valid_auth()
