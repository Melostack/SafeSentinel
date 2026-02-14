import unittest
import os
import json
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from api.server import app

class TestAPISecurity(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('api.server.Gatekeeper')
    def test_check_exception_handling(self, MockGatekeeper):
        # Simulate an internal error in Gatekeeper
        instance = MockGatekeeper.return_value
        instance.validate_address_format.side_effect = Exception("Sensitive Internal Error")

        payload = {
            "asset": "USDT",
            "origin": "Binance",
            "destination": "MetaMask",
            "network": "TRC20",
            "address": "T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb"
        }

        response = self.client.post("/check", json=payload)

        # Verify status code is 500
        self.assertEqual(response.status_code, 500)

        # Verify response body does NOT contain the sensitive error
        self.assertNotIn("Sensitive Internal Error", response.text)
        self.assertIn("Internal Server Error", response.text)

    @patch('api.server.SourcingAgent')
    def test_find_token_exception_handling(self, MockSourcingAgent):
        # Simulate an internal error in SourcingAgent
        instance = MockSourcingAgent.return_value
        instance.find_best_route.side_effect = Exception("Another Sensitive Error")

        payload = {
            "token": "USDT",
            "network": "ETH"
        }

        response = self.client.post("/find-token", json=payload)

        self.assertEqual(response.status_code, 500)
        self.assertNotIn("Another Sensitive Error", response.text)
        self.assertIn("Internal Server Error", response.text)

if __name__ == '__main__':
    unittest.main()
