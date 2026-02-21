
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust path to include root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.server import app

client = TestClient(app)

def test_auth_enforcement():
    """Verify that authentication is enforced."""

    # Mock dependencies to avoid side effects
    with patch('api.server.Gatekeeper') as MockGatekeeper, \
         patch('api.server.Humanizer') as MockHumanizer, \
         patch('api.server.OnChainVerifier') as MockVerifier, \
         patch.dict(os.environ, {"SAFE_SENTINEL_API_KEY": "test-secret-key"}):

        # Setup mocks for success path
        gk_instance = MockGatekeeper.return_value
        gk_instance.check_compatibility.return_value = {
            "status": "SAFE", "risk": "LOW", "message": "Safe"
        }
        MockVerifier.return_value.verify_address.return_value = {"status": "SUCCESS"}

        # 1. Test Missing Header -> Should fail
        resp_missing = client.post("/check", json={
            "asset": "USDT", "origin": "Binance", "destination": "Metamask", "network": "ERC20", "address": "0x123"
        })
        assert resp_missing.status_code == 403, f"Expected 403 for missing key, got {resp_missing.status_code}"

        # 2. Test Invalid Key -> Should fail
        resp_invalid = client.post("/check", headers={"X-API-Key": "wrong-key"}, json={
            "asset": "USDT", "origin": "Binance", "destination": "Metamask", "network": "ERC20", "address": "0x123"
        })
        assert resp_invalid.status_code == 403, f"Expected 403 for invalid key, got {resp_invalid.status_code}"

        # 3. Test Valid Key -> Should pass
        resp_valid = client.post("/check", headers={"X-API-Key": "test-secret-key"}, json={
            "asset": "USDT", "origin": "Binance", "destination": "Metamask", "network": "ERC20", "address": "0x123"
        })
        assert resp_valid.status_code == 200, f"Expected 200 for valid key, got {resp_valid.status_code}"

        print("Authentication verified: Enforced correctly.")

if __name__ == "__main__":
    try:
        test_auth_enforcement()
    except AssertionError as e:
        print(f"Assertion failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
