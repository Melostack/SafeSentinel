import unittest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from api.server import app, get_gatekeeper, get_humanizer, get_verifier

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

        # Create mocks
        self.mock_gatekeeper = MagicMock()
        self.mock_humanizer = MagicMock()
        self.mock_verifier = MagicMock()

        # Override dependencies
        app.dependency_overrides[get_gatekeeper] = lambda: self.mock_gatekeeper
        app.dependency_overrides[get_humanizer] = lambda: self.mock_humanizer
        app.dependency_overrides[get_verifier] = lambda: self.mock_verifier

    def tearDown(self):
        app.dependency_overrides = {}

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "SafeSentinel Command Center API Operational"})

    def test_check_transfer_safe(self):
        # Setup mock return values
        self.mock_verifier.verify_address.return_value = {
            "status": "SUCCESS", "is_contract": False, "type": "Personal Wallet"
        }
        self.mock_gatekeeper.check_compatibility.return_value = {
            "status": "SAFE", "risk": "LOW", "message": "Safe"
        }

        payload = {
            "asset": "USDT",
            "origin": "binance",
            "destination": "0x123",
            "network": "BSC",
            "address": "0x123"
        }

        response = self.client.post("/check", json=payload)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "SAFE")
        self.assertEqual(data["risk_level"], "LOW")

        # Verify calls
        self.mock_verifier.verify_address.assert_called_once()
        self.mock_gatekeeper.check_compatibility.assert_called_once()
        self.mock_humanizer.humanize_risk.assert_not_called()

    def test_check_transfer_unsafe(self):
        # Setup mock return values
        self.mock_verifier.verify_address.return_value = {
            "status": "SUCCESS"
        }
        self.mock_gatekeeper.check_compatibility.return_value = {
            "status": "UNSAFE", "risk": "HIGH", "message": "Risk"
        }
        self.mock_humanizer.humanize_risk.return_value = "Humanized Risk Explanation"

        payload = {
            "asset": "USDT",
            "origin": "binance",
            "destination": "0x123",
            "network": "BSC",
            "address": "0x123"
        }

        response = self.client.post("/check", json=payload)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "UNSAFE")
        self.assertEqual(data["message"], "Humanized Risk Explanation")

        # Verify calls
        self.mock_humanizer.humanize_risk.assert_called_once()

    def test_extract_intent(self):
        self.mock_humanizer.extract_intent.return_value = {"intent": "transfer"}

        response = self.client.post("/extract", json={"text": "send 100 usdt"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"intent": "transfer"})

if __name__ == "__main__":
    unittest.main()
