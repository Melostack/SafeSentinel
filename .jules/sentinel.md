## 2025-03-05 - [Missing Authentication and Secure Error Handling]
**Vulnerability:** The sensitive `/check` endpoint in `api/server.py` lacked authentication and returned raw exception messages in the HTTP 500 response, leaking internal stack traces.
**Learning:** Endpoints that execute sensitive operations like querying On-Chain data or executing Business Logic must always validate identity to prevent abuse and carefully handle unexpected errors to not expose internal system details.
**Prevention:** Implementing a secure dependency with FastAPI's `Security` and `APIKeyHeader` coupled with `secrets.compare_digest` to prevent timing attacks. Replacing raw `Exception` text with generic user-friendly strings and safely logging the full stack internally via `logging.error`.
