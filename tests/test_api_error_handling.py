import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)

class TestApiErrorHandling(unittest.TestCase):
    @patch('core.gatekeeper.Gatekeeper.check_compatibility')
    @patch('core.connectors.web3_rpc_connector.OnChainVerifier.verify_address')
    def test_check_endpoint_exception_leak(self, mock_verify, mock_check):
        # Setup mock to raise exception
        mock_check.side_effect = Exception("Sensitive internal error")
        mock_verify.return_value = {"balance": 0}

        payload = {
            "asset": "USDT",
            "origin": "Binance",
            "destination": "MetaMask",
            "network": "ERC20",
            "address": "0x1234567890abcdef1234567890abcdef12345678"
        }

        response = client.post("/check", json=payload)

        # Verify status code is 500
        self.assertEqual(response.status_code, 500)

        # Verify the generic error message
        self.assertEqual(response.json(), {"detail": "Internal Server Error"})

if __name__ == '__main__':
    unittest.main()
