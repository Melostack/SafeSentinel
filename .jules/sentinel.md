## 2026-04-04 - [Information Leakage in API Error Handling]
**Vulnerability:** The FastAPI endpoints `/check` and `/extract` were catching unhandled exceptions and returning their raw string representations directly to the client via `detail=str(e)`.
**Learning:** This exposes internal server details, stack traces, and potentially sensitive environment variables or connection strings to external users, violating the principle of failing securely.
**Prevention:** Always log the full exception internally (using `logger.error(e, exc_info=True)`) and return generic error messages (e.g., 'Internal server error') to the client in production APIs.
