import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from api.server import app

class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('api.server.Gatekeeper')
    def test_internal_server_error_leakage(self, MockGatekeeper):
        # Simulate an exception in Gatekeeper
        mock_instance = MockGatekeeper.return_value
        # We mock check_compatibility to raise an exception
        mock_instance.check_compatibility.side_effect = Exception("Secret Database Info")

        payload = {
            "asset": "USDT",
            "origin": "Binance",
            "destination": "0x123",
            "network": "ERC20",
            "address": "0x123"
        }

        response = self.client.post("/check", json=payload)

        # Verify status code
        self.assertEqual(response.status_code, 500)

        # Verify response body does NOT contain secret info
        self.assertEqual(response.json(), {"detail": "Internal Server Error"})
        self.assertNotIn("Secret Database Info", response.text)

if __name__ == '__main__':
    unittest.main()
