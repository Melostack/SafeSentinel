## 2024-05-24 - API Unbounded Input and Information Leakage Fix
**Vulnerability:** Pydantic models `CheckRequest` and `IntentRequest` lacked field limits, creating potential unbounded input vulnerabilities (DoS). `/check` endpoint exception handler returned raw exception strings (`detail=str(e)`), risking exposure of internal stack traces or database errors.
**Learning:** In FastAPI, default `str` fields in Pydantic models are unbounded. Unhandled exceptions that are caught and passed directly to the client can reveal system details.
**Prevention:** Enforce string lengths using `pydantic.Field(..., max_length=N)` for all incoming API data. Catch generic exceptions, log the full stack trace (`exc_info=True`) internally, and return a sanitized, non-specific error message to the client.
