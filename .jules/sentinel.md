## 2024-05-20 - API Server Information Leakage and Permissive CORS
**Vulnerability:** The API server had permissive CORS (`allow_origins=["*"]`) and leaked raw exception details in HTTP 500 responses (`detail=str(e)`).
**Learning:** These patterns expose the application to cross-origin attacks and leak internal architectural details. Error details must be logged internally but masked in API responses.
**Prevention:** Use environment variables to strictly limit CORS origins (`FRONTEND_URL`) and use Python's `logging` module to log exceptions internally while returning generic error messages to unauthenticated clients.
