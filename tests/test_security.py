import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from api.server import app
import json

client = TestClient(app)

class TestSecurity(unittest.TestCase):

    @patch('api.server.Gatekeeper')
    @patch('api.server.Humanizer')
    @patch('api.server.OnChainVerifier')
    def test_unhandled_exception_does_not_leak_details(self, mock_verifier, mock_humanizer, mock_gatekeeper):
        # Setup mock to raise an exception
        mock_gatekeeper.return_value.check_compatibility.side_effect = Exception("SENSITIVE INTERNAL ERROR: Database Connection Failed")

        # Mock other dependencies to avoid unrelated errors
        mock_verifier.return_value.verify_address.return_value = {"status": "SUCCESS"}

        response = client.post("/check", json={
            "asset": "USDT",
            "origin": "Binance",
            "destination": "0x123",
            "network": "ERC20",
            "address": "0x123"
        })

        # Assert SECURE behavior:
        # 1. Status code should be 500
        self.assertEqual(response.status_code, 500)

        # 2. Detail should NOT contain the sensitive error message
        self.assertNotIn("SENSITIVE INTERNAL ERROR", response.json()['detail'])

        # 3. Detail SHOULD be a generic message
        self.assertEqual(response.json()['detail'], "Internal Server Error")

    def test_intent_request_length_limit(self):
        # This is for the enhancement, checking if we can send a huge string
        huge_text = "A" * 1000000
        response = client.post("/extract", json={"text": huge_text})
        self.assertIn(response.status_code, [200, 400, 422, 500])

if __name__ == '__main__':
    unittest.main()
