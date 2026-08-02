## 2024-08-02 - Ensure API Exception Handlers Do Not Leak Internal State
**Vulnerability:** The exception handler in `api/server.py`'s `/check` endpoint previously returned `str(e)` in an HTTP 500 response, leaking internal stack traces and error details directly to the client. This is a severe information disclosure vulnerability.
**Learning:** Even internal routing systems must fail securely, especially when handling errors in Python's generic `Exception` catch block, as underlying dependencies (like RPC clients) may raise complex exceptions exposing infrastructure details.
**Prevention:** Exception handlers must log the exact error internally using `logging.error(..., exc_info=True)` and return a generic, non-sensitive string (e.g. "Erro interno do servidor") in the HTTP response.
