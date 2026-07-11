## 2024-05-24 - DoS through unbounded input fields and Info Leakage in API
**Vulnerability:** The FastAPI endpoint `/check` returned stack traces to users on exceptions, and the Pydantic models had no length limits, exposing the server to DoS attacks. Also, CORS was overly permissive (`["*"]`).
**Learning:** Even internal-facing unauthenticated APIs that expose generic tools must have length limits and secure error handling to prevent exploitation.
**Prevention:** Always use `Field(..., max_length=N)` for string inputs in Pydantic models, handle exceptions generically, and restrict CORS to `FRONTEND_URL`.
