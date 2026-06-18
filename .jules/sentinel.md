## 2024-03-24 - [CRITICAL] Prevent API information leakage, Unbounded inputs, and permissive CORS
**Vulnerability:** The API had three security flaws in `api/server.py`:
1.  **CORS misconfiguration:** `allow_origins=["*"]` allowed requests from any origin, violating security principles.
2.  **Unbounded Pydantic models:** `CheckRequest` and `IntentRequest` lacked field limits, creating a DoS risk via massive string payloads.
3.  **Information Leakage in Exception Handler:** The global catch block `except Exception as e` leaked raw stack trace strings directly to the client (`detail=str(e)`).
**Learning:** These three flaws expose endpoints to multiple attack vectors: cross-origin exploitation, denial of service via memory exhaustion, and exposure of internal architecture details useful for secondary attacks.
**Prevention:**
1.  Use `FRONTEND_URL` environment variable for `allow_origins`.
2.  Always use `Field(..., max_length=X)` on text fields in Pydantic models.
3.  Log exceptions internally (`logging.error("...", exc_info=True)`) and return generic 500 error messages (e.g., "Internal server error") to the client.