## 2024-05-17 - Information Leakage, Permissive CORS & DoS via Unbounded Input
**Vulnerability:** The API server returned raw exception details in HTTP 500 error responses (`detail=str(e)`). The CORS configuration was extremely permissive (`allow_origins=["*"]`). And the input models did not enforce length constraints on strings, opening vectors for application layer DoS.
**Learning:** These three components created a large attack surface. Leaking exception messages can give an attacker sensitive insights into internal architecture or state. Unrestricted CORS exposes users to cross-origin attacks. Unbounded inputs in Pydantic models expose endpoints to memory consumption via excessively long payloads.
**Prevention:**
- Only log raw exception details internally using `logging.error(e, exc_info=True)` and present generic user-friendly messages for 500 errors.
- Never use `allow_origins=["*"]` in production. Always restrict `allow_origins` to known domain origins, typically utilizing environment variables like `FRONTEND_URL`.
- Explicitly configure maximum length boundaries for all incoming string inputs utilizing Pydantic's `Field(..., max_length=X)`.