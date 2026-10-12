## 2024-05-24 - Secure Exception Handling in API Endpoints
**Vulnerability:** Unhandled exceptions were exposing raw error details (`detail=str(e)`) to API consumers, which could leak sensitive internal application states or stack traces.
**Learning:** Exposing raw exceptions directly in HTTP responses is an information leakage risk.
**Prevention:** Always log the exception details internally using `logging.error(..., exc_info=True)` and return generic, non-sensitive error messages to the client.
