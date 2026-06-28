## 2024-06-28 - [Information Leakage] Exposing exception details in API responses
**Vulnerability:** The `/check` endpoint in `api/server.py` was returning raw exception strings (e.g., `str(e)`) directly to the client when an error occurred, potentially leaking sensitive internal system details like stack traces, database states, or underlying infrastructure errors.
**Learning:** Returning `detail=str(e)` in HTTP exceptions is a common pattern that leaks sensitive information. Error handling must be secure by default.
**Prevention:** Exception handlers in API endpoints must log the error internally using `exc_info=True` and return generic, non-sensitive messages to prevent information leakage, rather than returning raw error strings.
