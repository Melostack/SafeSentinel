## 2024-05-24 - [Information Leakage in API Error Handling]
**Vulnerability:** The `/check` endpoint in `api/server.py` was catching general exceptions and returning `str(e)` directly to the client via a 500 HTTP response. This risks exposing sensitive information like internal stack traces or connection details.
**Learning:** Exception handlers in API endpoints must not return raw error strings.
**Prevention:** Always log the error internally using `exc_info=True` and return generic, non-sensitive messages to the client.
