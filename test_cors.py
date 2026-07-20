from fastapi.testclient import TestClient
import os

# Set FRONTEND_URL to a test value
os.environ["FRONTEND_URL"] = "http://test-frontend.com,https://another-frontend.com"

# Import app after setting env var
from api.server import app

client = TestClient(app)

def test_cors():
    response = client.options(
        "/",
        headers={
            "Origin": "http://test-frontend.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://test-frontend.com"
    print("CORS test passed for valid origin!")

if __name__ == "__main__":
    test_cors()
