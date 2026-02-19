import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from api.server import app

class TestInfoLeak(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_extract_info_leak(self):
        # Mock Humanizer to raise an exception with sensitive info
        with patch('core.humanizer.Humanizer.extract_intent') as mock_extract:
            mock_extract.side_effect = Exception("DB_PASSWORD=secret123 connection failed")

            response = self.client.post("/extract", json={"text": "test"})

            print(f"EXTRACT: Status Code: {response.status_code}")
            print(f"EXTRACT: Response Body: {response.json()}")

            # Verify leak
            self.assertEqual(response.status_code, 500)
            self.assertIn("Internal Server Error", response.json()['detail'])
            self.assertNotIn("DB_PASSWORD=secret123", str(response.json()))

    def test_check_info_leak(self):
        # Mock Gatekeeper to raise an exception with sensitive info
        with patch('core.gatekeeper.Gatekeeper.check_compatibility') as mock_check:
            mock_check.side_effect = Exception("SENSITIVE_KEY=12345 leaked in stack trace")

            # Also need to mock OnChainVerifier because check_transfer calls it first
            with patch('core.connectors.web3_rpc_connector.OnChainVerifier.verify_address') as mock_rpc:
                 mock_rpc.return_value = {} # Mock successful RPC call

                 payload = {
                     "asset": "USDT",
                     "origin": "Binance",
                     "destination": "Wallet",
                     "network": "ERC20",
                     "address": "0x123"
                 }

                 response = self.client.post("/check", json=payload)

                 print(f"CHECK: Status Code: {response.status_code}")
                 print(f"CHECK: Response Body: {response.json()}")

                 # Verify leak
                 self.assertEqual(response.status_code, 500)
                 self.assertIn("Internal Server Error", response.json()['detail'])
                 self.assertNotIn("SENSITIVE_KEY=12345", str(response.json()))

if __name__ == "__main__":
    unittest.main()
