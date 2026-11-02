## 2024-11-02 - Secure Exception Handling in API Endpoints
**Vulnerability:** Unhandled exceptions in `api/server.py` (specifically `/check`) were returning raw error strings (`detail=str(e)`) to the client, creating a risk of information leakage.
**Learning:** Returning `str(e)` directly in HTTP responses can expose internal system states, stack details, or underlying library errors which attackers can use for reconnaissance.
**Prevention:** Always log exceptions internally using `exc_info=True` and return sanitized, generic error messages to unauthenticated clients.
