## 2024-05-23 - [Information Leakage in Exception Handling]
**Vulnerability:** Raw exception details (`str(e)`) were being returned directly to the client in `api/server.py`'s `check_transfer` endpoint.
**Learning:** Returning raw exception details in HTTP 500 responses can expose internal system state, file paths, logic errors, or external API responses that an attacker can leverage for further exploitation.
**Prevention:** Always catch exceptions securely. Log the full details (`logging.error(e, exc_info=True)`) for debugging, but only return a generic error message (e.g., "Internal Server Error") to the client.

## 2024-05-23 - [Insecure CORS Configuration]
**Vulnerability:** The `CORSMiddleware` in `api/server.py` had `allow_origins=["*"]`, allowing any domain to perform cross-origin requests to the API.
**Learning:** While convenient for development, a wildcard origin allows malicious sites to read data from the API on behalf of authenticated users or in restricted networks, breaking same-origin policy assumptions.
**Prevention:** Restrict `allow_origins` to explicitly trusted domains using environment variables (e.g., `os.getenv("FRONTEND_URL", "http://localhost:3000")`) to ensure secure defaults.

## 2024-05-23 - [Unbounded Data Input Vulnerability]
**Vulnerability:** Pydantic models (`CheckRequest`, `IntentRequest`) lacked `max_length` constraints on string fields.
**Learning:** Processing unbounded string inputs can lead to Denial of Service (DoS) attacks, where malicious payloads consume excessive memory or CPU during JSON parsing, validation, or string manipulation.
**Prevention:** Always apply strict, reasonable upper bounds to external inputs using `pydantic.Field(..., max_length=N)`.
