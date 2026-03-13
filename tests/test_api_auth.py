import os
import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Set env var before importing app to avoid startup errors
os.environ["SAFE_SENTINEL_API_KEY"] = "test-secret-key"
os.environ["ALLOWED_ORIGINS"] = "http://testserver"

from api.server import app

class TestAPIAuth(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.api_key = "test-secret-key"
        self.headers = {"X-API-Key": self.api_key}

    def test_health_check_public(self):
        """Test that the root endpoint is public."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "SafeSentinel Command Center API Operational"})

    def test_extract_missing_auth(self):
        """Test accessing /extract without API key."""
        response = self.client.post("/extract", json={"text": "Hello"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "Could not validate credentials"})

    def test_extract_invalid_auth(self):
        """Test accessing /extract with wrong API key."""
        response = self.client.post("/extract", json={"text": "Hello"}, headers={"X-API-Key": "wrong-key"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "Could not validate credentials"})

    @patch("api.server.Humanizer")
    def test_extract_valid_auth(self, MockHumanizer):
        """Test accessing /extract with valid API key."""
        mock_hm = MockHumanizer.return_value
        mock_hm.extract_intent.return_value = {"intent": "test"}

        response = self.client.post("/extract", json={"text": "Hello"}, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"intent": "test"})

    def test_check_missing_auth(self):
        """Test accessing /check without API key."""
        response = self.client.post("/check", json={
            "asset": "USDT", "origin": "Binance", "destination": "Metamask",
            "network": "ETH", "address": "0x123"
        })
        self.assertEqual(response.status_code, 403)

    @patch("api.server.Gatekeeper")
    @patch("api.server.Humanizer")
    @patch("api.server.OnChainVerifier")
    def test_check_valid_auth(self, MockVerifier, MockHumanizer, MockGatekeeper):
        """Test accessing /check with valid API key."""
        # Mock dependencies to avoid actual logic execution
        mock_rpc = MockVerifier.return_value
        mock_rpc.verify_address.return_value = {"valid": True}

        mock_gk = MockGatekeeper.return_value
        mock_gk.check_compatibility.return_value = {"status": "SAFE", "risk": "LOW"}

        response = self.client.post("/check", json={
            "asset": "USDT", "origin": "Binance", "destination": "Metamask",
            "network": "ETH", "address": "0x123"
        }, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "SAFE")

if __name__ == "__main__":
    unittest.main()
