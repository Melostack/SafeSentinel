## 2024-03-24 - DoS and Information Leakage in API Endpoints
**Vulnerability:** Fast API Pydantic models lacked string length boundaries (`max_length`), and `Exception` handlers in API endpoints (`/check`, `/extract`) directly returned raw stack traces / error messages using `detail=str(e)`. The CORS middleware was also misconfigured to allow all origins (`allow_origins=["*"]`).
**Learning:** Returning `str(e)` on unhandled exceptions exposes internal application details to unauthenticated users. Missing input boundaries (like `max_length` in Pydantic) allows unbounded string payloads that can cause DoS. Allowing `*` in CORS defeats origin restrictions.
**Prevention:**
1. Always enforce string limits in Pydantic models using `Field(..., max_length=X)`.
2. Exception handlers in API endpoints must log the error internally using `exc_info=True` and return generic, non-sensitive messages to prevent information leakage, rather than returning raw error strings (e.g., `detail=str(e)`).
3. Use environment variables (like `FRONTEND_URL`) to restrict CORS explicitly.