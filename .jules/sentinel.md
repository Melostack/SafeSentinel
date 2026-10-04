## 2024-01-01 - Information Leakage in API Exceptions
**Vulnerability:** The FastAPI application was returning raw exception strings (`str(e)`) to the client, which could leak sensitive internal states, API keys, or database credentials.
**Learning:** Default error handlers in Python/FastAPI will reflect internal messages if not explicitly masked, posing a critical data exposure risk. Exception handlers in API endpoints must log the error internally using `exc_info=True` and return generic, non-sensitive messages.
**Prevention:** Always mask unhandled exceptions with a generic user-facing message (e.g. 'Erro interno do servidor') and log the raw error and traceback internally using `logging.error` with `exc_info=True`.
