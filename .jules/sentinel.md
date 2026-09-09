## 2024-05-18 - [Prevent Information Leakage]
**Vulnerability:** Unhandled exceptions exposed raw error messages (including potential stack traces) via `detail=str(e)` in the `/check` endpoint.
**Learning:** Exception details can leak sensitive backend infrastructure information to unauthenticated clients.
**Prevention:** Use `logging.error(..., exc_info=True)` internally and return generic, non-sensitive error messages to clients.
