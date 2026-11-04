## 2024-05-24 - Fix information leakage in exception handler
**Vulnerability:** The exception handler in `/check` exposed raw error strings directly to the client via `detail=str(e)`.
**Learning:** Exception messages can contain sensitive internal system details like paths, module names, or database queries.
**Prevention:** Always log exceptions internally using `exc_info=True` and return a generic error message (e.g., "Erro interno do servidor") to the client.
