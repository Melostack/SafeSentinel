## 2024-05-15 - Information Leakage in API Exception Handlers
**Vulnerability:** Unhandled exceptions in the API endpoints were returning raw error strings (e.g., `str(e)`) to the client, exposing sensitive stack traces and internal details.
**Learning:** Always fail securely by catching exceptions, logging the internal error for debugging purposes, and returning generic error messages to unauthenticated clients.
**Prevention:** Ensure that all global exception handlers use `logging.error(..., exc_info=True)` and raise generic `HTTPException`s rather than exposing internal errors.
