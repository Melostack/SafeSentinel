## 2024-05-15 - Information Exposure via Exception Handling
**Vulnerability:** The API endpoint (`/check` in `api/server.py`) returned the raw exception string to the client (`raise HTTPException(..., detail=str(e))`) upon encountering an error, which can expose internal stack traces or sensitive system configuration.
**Learning:** Exception handling in public-facing APIs must not bubble up raw internal exceptions. They must be caught, logged internally, and a generic user-friendly message returned.
**Prevention:** Always use internal logging (e.g. `logging.error(..., exc_info=True)`) to preserve the trace for debugging, and return generic messages like "Internal server error" in the HTTP response.
