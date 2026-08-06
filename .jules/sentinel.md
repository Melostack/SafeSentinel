## 2024-05-18 - API Security Flaws: CORS, DoS, and Info Leakage
**Vulnerability:** Overly permissive CORS `allow_origins=["*"]`, missing string length limits in Pydantic models, and raw exception details returned in 500 errors.
**Learning:** Returning `str(e)` in HTTP exceptions exposes internal stack traces and environment states. Leaving Pydantic string fields unbounded enables DoS via large payloads. Global CORS allows cross-origin exploitation.
**Prevention:** Always use environment-driven CORS whitelisting (e.g., `FRONTEND_URL`), enforce `max_length` using Pydantic's `Field` for string inputs, and log exceptions internally with `exc_info=True` while returning generic messages like "Erro interno do servidor" to users.
