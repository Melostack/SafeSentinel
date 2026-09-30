## 2026-09-30 - Fix Information Leakage
**Vulnerability:** API exceptions were returning raw error strings via `detail=str(e)`, exposing internal implementation details and stack traces.
**Learning:** Exception handlers in API endpoints must log the error internally and return generic messages.
**Prevention:** Always log internal errors with `exc_info=True` and return generic error messages (e.g., "Erro interno do servidor").
