import unittest
from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)

class TestAPIValidation(unittest.TestCase):
    def test_check_request_validation_asset_too_long(self):
        # Asset length > 50
        payload = {
            "asset": "A" * 51,
            "origin": "Binance",
            "destination": "Wallet",
            "network": "Ethereum",
            "address": "0x123"
        }
        response = client.post("/check", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_check_request_validation_address_too_long(self):
        # Address length > 100
        payload = {
            "asset": "USDT",
            "origin": "Binance",
            "destination": "Wallet",
            "network": "Ethereum",
            "address": "0x" + "1" * 100
        }
        response = client.post("/check", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_intent_request_validation_text_too_long(self):
        # Text length > 1000
        payload = {
            "text": "A" * 1001
        }
        response = client.post("/extract", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_valid_request(self):
        # Valid payload should NOT return 422
        # It might return 200 or 500 depending on backend state, but definitely not 422
        payload = {
            "asset": "USDT",
            "origin": "Binance",
            "destination": "Wallet",
            "network": "Ethereum",
            "address": "0x123"
        }
        response = client.post("/check", json=payload)
        self.assertNotEqual(response.status_code, 422)

if __name__ == '__main__':
    unittest.main()
