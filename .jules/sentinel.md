## 2024-08-07 - Information Leakage in API Exception Handlers
**Vulnerability:** The FastAPI endpoint `/check` catches unhandled exceptions and returns `str(e)` directly to the client via HTTP 500 responses. This exposes internal server state, stack details, and potentially sensitive environment variables or file paths.
**Learning:** The default pattern in this codebase for handling FastAPI exceptions was to naively return the exception string, bypassing secure logging practices.
**Prevention:** All exception handlers must log the full exception internally (using `exc_info=True`) and return a generic, non-sensitive error message (e.g., "Erro interno do servidor") to the client.
