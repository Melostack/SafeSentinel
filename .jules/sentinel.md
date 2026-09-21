## 2024-05-24 - Information Leakage in Error Messages
**Vulnerability:** The API returned raw exception strings (`str(e)`) to clients on HTTP 500 errors, exposing potentially sensitive internal system details.
**Learning:** Returning unhandled or raw exceptions directly in the response payload is a critical information leakage vector that can aid attackers.
**Prevention:** Catch generic exceptions, log them internally (e.g., with `exc_info=True`), and return a safe, generic error message (e.g., "Erro interno do servidor") to the client.