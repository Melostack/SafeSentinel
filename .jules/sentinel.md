## 2024-05-20 - Exposing Sensitive Data in Exception Handlers
**Vulnerability:** The `/check` endpoint in `api/server.py` returned raw exception strings (`str(e)`) to the client, which could leak internal stack traces and sensitive environment details (Critical severity).
**Learning:** Exception details must be sanitized at the boundary to prevent information leakage. Internal APIs consumed by unauthenticated clients shouldn't expose backend state.
**Prevention:** Use standard `logging` with `exc_info=True` for internal visibility, and always return generic error messages (e.g., "Erro interno do servidor") for 500-level HTTP responses.
