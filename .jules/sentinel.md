## 2024-05-27 - Fix Information Leakage in API Error Handler
**Vulnerability:** The `/check` endpoint in `api/server.py` exposed internal stack traces and server-side errors to the client by returning `str(e)` in an `HTTPException(status_code=500, detail=str(e))` inside a generic catch-all `except Exception as e:` block.
**Learning:** Returning `str(e)` can leak sensitive infrastructure details like database credentials or server configurations. Error handlers in API endpoints must log the actual error internally and return generic messages to the client.
**Prevention:** Always log exceptions using `exc_info=True` to preserve tracebacks internally, and raise HTTP exceptions with a safe, non-revealing `detail` message to the client.
