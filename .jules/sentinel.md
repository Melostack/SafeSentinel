## 2024-05-24 - [Information Exposure in API Exception Handler]
**Vulnerability:** The `/check` API endpoint caught generic exceptions (`except Exception as e:`) and directly returned the error string (`str(e)`) to the client via a 500 HTTP response. This could leak internal stack traces, system information, or credentials.
**Learning:** Returning `str(e)` in Python APIs without filtering or sanitizing exposes unhandled internals directly to unauthenticated clients. Standard FastAPI error handling might not hide these without explicit configuration or generic fallbacks.
**Prevention:** Exception handlers must log the error internally (e.g., using `logger.error(..., exc_info=True)`) and return a safe, generic message to the client (e.g., "Erro interno do servidor").
