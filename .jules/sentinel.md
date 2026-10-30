## 2023-10-30 - [Information Leakage in API Error Handler]
**Vulnerability:** The `/check` endpoint in `api/server.py` was returning the raw exception string (`detail=str(e)`) in the HTTP 500 response, potentially leaking internal server details or stack traces to unauthenticated clients.
**Learning:** Always use generic error messages for unhandled exceptions in public-facing APIs, and log the detailed error internally.
**Prevention:** Use a standard logger with `exc_info=True` for internal tracking and return a non-sensitive message like "Erro interno do servidor" to the client.