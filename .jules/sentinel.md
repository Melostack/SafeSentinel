## 2026-05-20 - Exception Leakage in API
**Vulnerability:** The FastAPI application was catching generic `Exception` and returning `str(e)` as the `detail` in `HTTPException(500)`. This leaked internal implementation details (e.g., file paths, library errors) to the client.
**Learning:** Developers often prioritize debugging ease (seeing the error) over security in early stages, but this creates a critical information disclosure risk in production.
**Prevention:** Always log the full exception internally (using `logging.exception`) and return a sanitized, generic error message (e.g., 'Internal Server Error') to the external client.
