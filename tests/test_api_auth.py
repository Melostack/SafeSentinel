
import os
import unittest
from fastapi.testclient import TestClient
from api.server import app

class TestAPIAuth(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Mock environment variable for the test
        os.environ["SAFE_SENTINEL_API_KEY"] = "test_secret_key"

    def test_public_endpoint(self):
        """Root endpoint should be public."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_extract_endpoint_no_auth(self):
        """/extract should require authentication."""
        response = self.client.post("/extract", json={"text": "hello"})
        # Currently this returns 200/500, but we want 403/401
        # For now, we assert what happens currently to confirm behavior,
        # but after fix, we will update this test.
        # Actually, let's write the test as it SHOULD BE after the fix,
        # so it fails now.
        self.assertIn(response.status_code, [401, 403])

    def test_check_endpoint_no_auth(self):
        """/check should require authentication."""
        response = self.client.post("/check", json={
            "asset": "USDT", "origin": "Binance", "destination": "Metamask",
            "network": "ERC20", "address": "0x123"
        })
        self.assertIn(response.status_code, [401, 403])

    def test_check_endpoint_with_auth(self):
        """/check should accept valid API key."""
        headers = {"X-API-Key": "test_secret_key"}
        # We expect 500 because dependencies (RPC/LLM) might fail or mock objects are needed,
        # but definitely NOT 401/403.
        response = self.client.post("/check", json={
            "asset": "USDT", "origin": "Binance", "destination": "Metamask",
            "network": "ERC20", "address": "0x123"
        }, headers=headers)
        self.assertNotEqual(response.status_code, 401)
        self.assertNotEqual(response.status_code, 403)

if __name__ == "__main__":
    unittest.main()
