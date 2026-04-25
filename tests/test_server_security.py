import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import os
import sys

# Mock dependencies before importing the app
sys.modules['core.gatekeeper'] = MagicMock()
sys.modules['core.humanizer'] = MagicMock()
sys.modules['core.sourcing_agent'] = MagicMock()
sys.modules['core.connectors.web3_rpc_connector'] = MagicMock()

from api.server import app

class TestServerSecurity(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('api.server.Gatekeeper')
    def test_check_endpoint_exception_handling(self, MockGatekeeper):
        # Force the gatekeeper to raise an exception
        mock_gk = MockGatekeeper.return_value
        mock_gk.check_compatibility.side_effect = Exception("Super secret database failure: root password is '12345'")

        payload = {
            "asset": "USDT",
            "origin": "Binance",
            "destination": "0x123",
            "network": "EVM",
            "address": "0x1234567890123456789012345678901234567890"
        }

        response = self.client.post("/check", json=payload)
        self.assertEqual(response.status_code, 500)
        self.assertNotIn("Super secret database failure", response.json()['detail'])
        self.assertEqual(response.json()['detail'], "An internal error occurred while processing your request.")

    def test_input_length_limits(self):
        # Try to send an extremely long string for asset to trigger 422 Unprocessable Entity
        payload = {
            "asset": "A" * 150, # Max is 100
            "origin": "Binance",
            "destination": "0x123",
            "network": "EVM",
            "address": "0x123"
        }
        response = self.client.post("/check", json=payload)
        self.assertEqual(response.status_code, 422)

if __name__ == '__main__':
    unittest.main()
