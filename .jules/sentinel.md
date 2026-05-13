## 2024-05-24 - Overly Permissive CORS and Exception Information Leakage
**Vulnerability:** The FastAPI server was configured with `allow_origins=["*"]` in the CORS middleware, allowing any origin to make cross-origin requests. Additionally, the `/check` endpoint's exception handler directly returned `str(e)`, exposing internal stack traces or internal exception details to the end-user. The Pydantic request models also lacked `max_length` limits, leading to potential DoS vulnerabilities from unbounded inputs.
**Learning:** Returning raw exception details is a significant security risk as it can leak database schema, internal logic, or stack traces. Unbounded model inputs allow payload-based Denial-of-Service attacks. Finally, allowing all origins (`*`) in CORS defeats its security benefits in web environments.
**Prevention:**
- Restrict `allow_origins` strictly to trusted domains (`FRONTEND_URL`).
- Use `logging.error("...", exc_info=True)` for internal debugging instead of exposing details to the client.
- Return generic HTTP 500 errors to the client.
- Always enforce `max_length` constraints on API inputs using Pydantic's `Field()`.
