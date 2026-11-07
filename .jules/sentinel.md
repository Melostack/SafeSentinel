## 2026-11-07 - Information Leakage via Exception Handler
**Vulnerability:** The `/check` endpoint was exposing internal system state, stack traces, and potential secrets by returning the raw exception string (`str(e)`) directly to the client in a 500 HTTP response.
**Learning:** Directly passing unhandled exception strings to the client creates an information leakage vector, potentially giving attackers insight into database connections, API keys, or backend architecture.
**Prevention:** Always log the full exception internally (e.g., `logging.error(..., exc_info=True)`) and return a sanitized, generic error message (e.g., "Erro interno do servidor") to the client.
