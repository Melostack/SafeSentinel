## 2024-05-24 - Fix API Security Vulnerabilities
**Vulnerability:** The API had multiple vulnerabilities: permissive CORS (`allow_origins=["*"]`), unbounded input on endpoints posing a DoS risk, and stack trace leakage in error responses.
**Learning:** These vulnerabilities are common patterns in initial API prototypes. The memory correctly highlighted the risks of unbounded input and raw error messages in production. Adding Pydantic `Field` restrictions and using `exc_info=True` with generic HTTP errors is critical for security.
**Prevention:** Always set CORS to specific domains (e.g., using ENV vars). Enforce `max_length` on all Pydantic strings. Never expose `str(e)` in a 500 response; log with `exc_info=True` and return a generic message.
