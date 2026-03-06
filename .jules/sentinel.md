## 2024-05-24 - API Error Handling exposes stack traces
**Vulnerability:** The `/check` endpoint in `api/server.py` catches general exceptions and returns `str(e)` directly to the user via a 500 status code (`raise HTTPException(status_code=500, detail=str(e))`). This can leak internal stack traces and error details, violating secure coding standards.
**Learning:** Returning `str(e)` in an exception handler allows internal system details to be exposed if an error occurs.
**Prevention:** Catch the exception, log it properly using `logging.error(e, exc_info=True)` to ensure developers have access to the traceback, and return a generic error message like `Internal server error` to the client.
