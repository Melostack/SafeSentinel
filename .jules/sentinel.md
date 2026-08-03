## 2024-05-24 - Exception Handling Information Disclosure
**Vulnerability:** The `/check` endpoint in `api/server.py` leaked internal error details by returning raw exception strings (`str(e)`) in HTTP 500 responses.
**Learning:** Returning `str(e)` in an exception handler allows a potential attacker to learn about the internal state, stack traces, and underlying libraries of the server if an unexpected failure occurs.
**Prevention:** Exception handlers must log the exact error securely using `exc_info=True` (e.g., with the standard `logging` module) and return a generic, non-sensitive message to the client (like "Erro interno do servidor").
