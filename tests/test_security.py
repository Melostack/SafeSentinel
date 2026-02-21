import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch
from api.server import app

class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("api.server.Gatekeeper")
    @patch("api.server.Humanizer")
    @patch("api.server.OnChainVerifier")
    def test_exception_leakage(self, MockVerifier, MockHumanizer, MockGatekeeper):
        # Setup mocks
        mock_gk = MockGatekeeper.return_value
        # Simulate a crash with sensitive info
        mock_gk.check_compatibility.side_effect = Exception("SENSITIVE_DB_INFO_LEAK")

        mock_rpc = MockVerifier.return_value
        mock_rpc.verify_address.return_value = {"valid": True}

        response = self.client.post("/check", json={
            "asset": "USDT",
            "origin": "Binance",
            "destination": "0x123",
            "network": "ETH",
            "address": "0x123"
        })

        # New behavior: 500 but generic message
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["detail"], "Internal Server Error")
        self.assertNotIn("SENSITIVE_DB_INFO_LEAK", response.json()["detail"])
