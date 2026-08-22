## 2024-08-22 - API Security Hardening (CORS, DoS, Error Leakage)
**Vulnerability:** The FastAPI server used wildcard CORS (`allow_origins=["*"]`), lacked string length limits on incoming Pydantic models, and returned raw exception messages in the `/check` endpoint.
**Learning:** Using wildcard CORS exposes the API to unauthorized domains. Lacking length limits opens the door to DoS via large payloads. Returning raw errors leaks internal implementation details.
**Prevention:** Use environment variables to strictly define `allow_origins`, use `pydantic.Field` for strict length limits, and log errors internally while returning generic user-facing messages.
