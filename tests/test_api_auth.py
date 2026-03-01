import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure we can import from root
sys.path.append(os.getcwd())

# Set env var for testing
os.environ["SAFE_SENTINEL_API_KEY"] = "test-secret"

from api.server import app

client = TestClient(app)

def test_extract_no_auth():
    response = client.post("/extract", json={"text": "hello"})
    assert response.status_code == 403
    assert response.json() == {"detail": "API Key missing"}

def test_extract_invalid_auth():
    response = client.post("/extract", json={"text": "hello"}, headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid API Key"}

def test_extract_valid_auth():
    # We expect 400 because Humanizer extraction might fail (no API key for Gemini) or logic error
    # But as long as it's not 403, auth worked.
    response = client.post("/extract", json={"text": "hello"}, headers={"X-API-Key": "test-secret"})
    assert response.status_code != 403

def test_check_no_auth():
    response = client.post("/check", json={
        "asset": "USDT",
        "origin": "Binance",
        "destination": "MetaMask",
        "network": "ERC20",
        "address": "0x123"
    })
    assert response.status_code == 403

def test_check_valid_auth():
    response = client.post("/check", json={
        "asset": "USDT",
        "origin": "Binance",
        "destination": "MetaMask",
        "network": "ERC20",
        "address": "0x123"
    }, headers={"X-API-Key": "test-secret"})
    assert response.status_code != 403
