import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from api.server import app
import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAPIAuth(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.valid_api_key = "test_api_key"
        os.environ["SAFE_SENTINEL_API_KEY"] = self.valid_api_key

    @patch("api.server.Humanizer")
    @patch("api.server.Gatekeeper")
    @patch("api.server.OnChainVerifier")
    def test_missing_api_key(self, mock_verifier, mock_gatekeeper, mock_humanizer):
        response = self.client.post("/check", json={
            "asset": "USDT",
            "origin": "Binance",
            "destination": "MetaMask",
            "network": "ERC20",
            "address": "0x1234567890123456789012345678901234567890"
        })
        # Expect 403 Forbidden because no API key is provided
        self.assertEqual(response.status_code, 403)

    @patch("api.server.Humanizer")
    @patch("api.server.Gatekeeper")
    @patch("api.server.OnChainVerifier")
    def test_invalid_api_key(self, mock_verifier, mock_gatekeeper, mock_humanizer):
        response = self.client.post("/check", json={
            "asset": "USDT",
            "origin": "Binance",
            "destination": "MetaMask",
            "network": "ERC20",
            "address": "0x1234567890123456789012345678901234567890"
        }, headers={"X-API-Key": "invalid_key"})
        # Expect 403 Forbidden because API key is invalid
        self.assertEqual(response.status_code, 403)

    @patch("api.server.Humanizer")
    @patch("api.server.Gatekeeper")
    @patch("api.server.OnChainVerifier")
    def test_valid_api_key(self, mock_verifier, mock_gatekeeper, mock_humanizer):
        # Setup mocks to return success
        mock_verifier_instance = mock_verifier.return_value
        mock_verifier_instance.verify_address.return_value = {"status": "SUCCESS", "is_contract": False}

        mock_gatekeeper_instance = mock_gatekeeper.return_value
        mock_gatekeeper_instance.check_compatibility.return_value = {"status": "SAFE", "risk": "LOW"}

        mock_humanizer_instance = mock_humanizer.return_value

        response = self.client.post("/check", json={
            "asset": "USDT",
            "origin": "Binance",
            "destination": "MetaMask",
            "network": "ERC20",
            "address": "0x1234567890123456789012345678901234567890"
        }, headers={"X-API-Key": self.valid_api_key})

        # Expect 200 OK because API key is valid
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
