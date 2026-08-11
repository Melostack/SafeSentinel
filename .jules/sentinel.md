## 2024-08-11 - Prevent Exception Detail Leakage in API Responses
**Vulnerability:** The FastAPI `/check` endpoint exception handler returned the raw error string (`str(e)`) in its 500 Internal Server Error response, potentially leaking sensitive internal server state or stack traces to clients.
**Learning:** Catch-all exception handlers must not blindly pass the original exception message to the user. This is a common pattern that leaks implementation details, posing an information disclosure risk.
**Prevention:** Ensure that all global or endpoint-level exception handlers log the detailed error internally (`exc_info=True`) and return a generic, non-sensitive error message (e.g., "Erro interno do servidor") to the client.
