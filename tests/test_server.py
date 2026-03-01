from fastapi.testclient import TestClient
from unittest.mock import patch
from api.server import app

client = TestClient(app)

def test_extract_intent_max_length():
    # Mock the extract_intent method to avoid external API calls
    with patch('core.humanizer.Humanizer.extract_intent') as mock_extract:
        mock_extract.return_value = {"intent": "test_intent"}

        # Test case: Text within limit (10 characters)
        short_text = "a" * 10
        response = client.post("/extract", json={"text": short_text})
        assert response.status_code == 200, f"Expected 200 for short text, got {response.status_code}"
        assert response.json() == {"intent": "test_intent"}

        # Test case: Text exceeding limit (1001 characters)
        long_text = "a" * 1001
        response = client.post("/extract", json={"text": long_text})

        # Ideally, this should be 422 after the fix.
        # Before the fix, it will be 200 (because the mock returns success) or 500.
        # So this assertion will fail before the fix.
        assert response.status_code == 422, f"Expected 422 for long text, got {response.status_code}"
