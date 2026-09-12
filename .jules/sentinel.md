## 2024-05-20 - [Fix Overly Permissive CORS and Info Leakage in FastAPI]
**Vulnerability:** FastAPI endpoints had overly permissive CORS (`allow_origins=["*"]`), no Pydantic string limits (DoS risk), and exception handlers leaked internal errors via `detail=str(e)`.
**Learning:** These represent a recurring pattern where default configurations lead to security risks in development and production (e.g. CSRF via CORS, resource exhaustion, and sensitive info leakage).
**Prevention:** Always restrict `allow_origins` to specific domains (via env vars), enforce `max_length` in Pydantic models, and use generic error messages for HTTP 500 responses while logging the actual exception internally.
