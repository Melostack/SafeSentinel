## 2025-06-04 - [Fix Overly Permissive CORS and Error Leakage in FastAPI]
**Vulnerability:** The FastAPI application (`api/server.py`) had a wildly permissive CORS configuration (`allow_origins=["*"]`), which allowed any website to make cross-origin requests to the API. Additionally, the `/check` endpoint's top-level error handler was returning the raw exception string to the client (`detail=str(e)`), risking the exposure of sensitive stack traces, file paths, or infrastructure details.
**Learning:** Development configurations often default to permissive settings (like wildcard CORS or verbose errors) to simplify testing, but these configurations must be hardened before deployment. Fast APIs should dynamically configure CORS based on the environment and ensure error messages are obfuscated and logged internally.
**Prevention:**
1. Use environment variables (like `FRONTEND_URL`) to explicitly whitelist allowed origins for CORS.
2. Always use `logging.error(..., exc_info=True)` for internal visibility and return generic HTTP exception messages to clients to prevent information leakage.
