
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust path to include root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.server import app

client = TestClient(app)

def test_exception_leak():
    # Mock Gatekeeper to raise an exception with sensitive info
    with patch('api.server.Gatekeeper') as MockGatekeeper, \
         patch.dict(os.environ, {"SAFE_SENTINEL_API_KEY": "test-secret-key"}):

        instance = MockGatekeeper.return_value
        # Raise an exception when check_compatibility is called
        instance.check_compatibility.side_effect = Exception("Database connection failed: user=admin password=SUPER_SECRET_PASSWORD host=10.0.0.1")

        response = client.post("/check", headers={"X-API-Key": "test-secret-key"}, json={
            "asset": "USDT",
            "origin": "Binance",
            "destination": "Metamask",
            "network": "ERC20",
            "address": "0x123"
        })

        assert response.status_code == 500
        # This confirms the vulnerability IS FIXED: the password is NOT leaked in the response
        detail = response.json()['detail']
        assert "SUPER_SECRET_PASSWORD" not in detail, f"Sensitive info leaked: {detail}"
        assert detail == "Internal Server Error", f"Expected generic error, got: {detail}"

        print("Security Verified: Exception message NOT leaked to client.")

if __name__ == "__main__":
    try:
        test_exception_leak()
    except AssertionError as e:
        print(f"Assertion failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
