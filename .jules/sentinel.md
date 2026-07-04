## 2024-07-04 - [High] Information Leakage and DoS Vectors in API
**Vulnerability:** The FastAPI server (`api/server.py`) exposed a few security risks:
1. Overly permissive CORS `allow_origins=["*"]`, enabling malicious domains to interact with the API if deployed with user-level auth.
2. Lack of length constraints in Pydantic models (DoS vector via large payloads parsing).
3. The global exception handler leaked full stack traces directly to the client via `detail=str(e)`.
**Learning:** These are common defaults when scaffolding an API that need explicit configuration before production deployment.
**Prevention:**
- Always configure CORS using environment variables for trusted domains.
- Validate bounds/length limits for all string fields in Pydantic schemas using `Field(..., max_length=X)`.
- Use `logger.error(..., exc_info=True)` for internal logging of unhandled exceptions, and return a sanitized, generic error message to the client.
