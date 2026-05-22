## 2024-05-30 - Fix CORS, input validation, and error handling in api/server.py
**Vulnerability:**
- Overly permissive CORS allowed any origin (`allow_origins=["*"]`).
- Missing input validation on Pydantic models `CheckRequest` and `IntentRequest` exposed the API to DoS risks.
- Raw error strings leaked via `HTTPException` detail.

**Learning:**
- CORS configuration must always be strictly tied to frontend environment variables (like `FRONTEND_URL`) to prevent CSRF/unauthorized access.
- Pydantic models must enforce `Field(..., max_length=X)` to prevent unbounded string payloads and DoS.
- Catch-all exception handlers must log internally using `exc_info=True` and mask external responses to avoid leaking stack traces or internal mechanics.

**Prevention:**
- Avoid `allow_origins=["*"]` by default. Implement environment variable-based CORS configurations.
- Enforce max lengths on all string inputs at the API boundary using Pydantic `Field`.
- Standardize error handling to return generic messages (`Erro interno do servidor`) while securely logging exceptions with full stack traces.
