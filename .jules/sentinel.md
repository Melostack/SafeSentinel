## 2024-05-24 - API Vulnerability Fixes (CORS, DoS, Information Leakage)
**Vulnerability:** The FastAPI application (`api/server.py`) was vulnerable to several issues:
1. **Overly Permissive CORS:** `allow_origins=["*"]` allowed any site to make cross-origin requests, a critical misconfiguration.
2. **Denial of Service (DoS):** Pydantic models for incoming requests lacked length constraints, opening the API up to DoS attacks with huge payloads.
3. **Information Leakage:** Exception handlers returned `str(e)` directly to the user via HTTP 500 responses, exposing internal stack traces or implementation details.
**Learning:** These are common backend development anti-patterns. Often during development, unrestricted CORS and verbose error messages are temporarily enabled but missed before shipping to production.
**Prevention:**
1. CORS settings should strictly use a whitelist of allowed domains (e.g., loaded via environment variables).
2. All string inputs in API requests (e.g., Pydantic models) should have strict `max_length` validations based on expected constraints.
3. Catch-all `except Exception` blocks must log the error securely internally (using `logging.error` with `exc_info=True`) and return a generic, non-informative error message to the client.