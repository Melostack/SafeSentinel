import unittest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import os
import sys

# Add project root to path so we can import api.server
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# We need to ensure we can import api.server
from api.server import app

class TestAPIAuth(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.valid_key = "test_secret_key"
        # Set the environment variable for the app to pick it up
        os.environ["SAFE_SENTINEL_API_KEY"] = self.valid_key

    def tearDown(self):
        if "SAFE_SENTINEL_API_KEY" in os.environ:
            del os.environ["SAFE_SENTINEL_API_KEY"]

    def test_home_public(self):
        # Home page should be public
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_extract_intent_no_key(self):
        response = self.client.post("/extract", json={"text": "some text"})
        self.assertEqual(response.status_code, 403)
        self.assertIn("Could not validate credentials", response.json()["detail"])

    def test_extract_intent_invalid_key(self):
        response = self.client.post("/extract", json={"text": "some text"}, headers={"X-API-Key": "wrong_key"})
        self.assertEqual(response.status_code, 403)
        self.assertIn("Could not validate credentials", response.json()["detail"])

    def test_extract_intent_valid_key(self):
        # Mock Humanizer to avoid external calls
        with patch('api.server.Humanizer') as MockHumanizer:
            mock_instance = MockHumanizer.return_value
            mock_instance.extract_intent.return_value = {"asset": "USDT"}

            response = self.client.post("/extract", json={"text": "some text"}, headers={"X-API-Key": self.valid_key})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"asset": "USDT"})

    def test_check_transfer_no_key(self):
        response = self.client.post("/check", json={
            "asset": "USDT", "origin": "Binance", "destination": "Metamask",
            "network": "ERC20", "address": "0x123"
        })
        self.assertEqual(response.status_code, 403)

    def test_check_transfer_valid_key(self):
        with patch('api.server.Gatekeeper') as MockGK, \
             patch('api.server.Humanizer') as MockHM, \
             patch('api.server.OnChainVerifier') as MockRPC:

            gk_instance = MockGK.return_value
            gk_instance.check_compatibility.return_value = {"status": "SAFE", "risk": "LOW"}

            rpc_instance = MockRPC.return_value
            rpc_instance.verify_address.return_value = {"status": "SUCCESS"}

            response = self.client.post("/check", json={
                "asset": "USDT", "origin": "Binance", "destination": "Metamask",
                "network": "ERC20", "address": "0x123"
            }, headers={"X-API-Key": self.valid_key})

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["status"], "SAFE")

if __name__ == '__main__':
    unittest.main()
