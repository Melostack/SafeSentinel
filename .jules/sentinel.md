## 2024-05-24 - [Information Leakage] Exception String Passed to Client
**Vulnerability:** The unhandled exception `str(e)` was passed into `HTTPException` detail and returned directly to the client in the API `/check` endpoint. This acts as an information leakage vulnerability, exposing stack trace details, variables, or system architecture information to an end user.
**Learning:** Exception handlers in Fast API endpoints should never return explicit error messages from python exceptions unless explicitly designed for external view.
**Prevention:** Internally log full exceptions (`logging.error("msg", exc_info=True)`) to maintain observability while returning generic messages (e.g. `500 Internal server error`) via HTTP handlers to maintain secure failures.
