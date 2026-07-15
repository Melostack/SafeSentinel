## 2024-05-24 - API Security Hardening (CORS, DoS, Error Leakage)
**Vulnerability:** The main `api/server.py` had several insecure defaults:
1. `allow_origins=["*"]` in CORS, allowing any domain to access the API.
2. Missing length limits on Pydantic `BaseModel` string fields (`CheckRequest`, `IntentRequest`), making the server vulnerable to resource exhaustion DoS attacks via extremely large inputs.
3. Catch-all `except Exception as e:` block returning `str(e)` directly to clients, potentially leaking internal stack traces or sensitive environment data.
**Learning:** Default configurations in frameworks (like permissive CORS or unbound string fields) are often optimized for development speed, not security. Explicit boundaries are required for production.
**Prevention:**
- Always bind `allow_origins` to a trusted list (e.g., via `FRONTEND_URL` env var).
- Always use Pydantic `Field(..., max_length=X)` for string inputs to enforce boundaries.
- Catch-all exception handlers must use `logging.error(..., exc_info=True)` for internal debugging and return generic, non-sensitive errors (e.g., "Erro interno do servidor") to clients.
