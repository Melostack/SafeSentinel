
## 2024-05-24 - API Security Vulnerabilities
**Vulnerability:** Found multiple vulnerabilities in `api/server.py`: overly permissive CORS configuration (`allow_origins=["*"]`), unbounded inputs in Pydantic models (DoS risk), and exception handlers returning raw error strings (stack trace/internal information leakage).
**Learning:** Default FastApi generated configurations and basic exception handlers often neglect input length restrictions, allow permissive CORS, and risk exposing sensitive info to external clients. These defaults should be audited when an app goes live.
**Prevention:**
1. Always enforce string limits using `Field(..., max_length=X)` in Pydantic models.
2. Ensure exception handlers in API endpoints log internal errors using `exc_info=True` and return generic, non-sensitive messages.
3. Configure `CORSMiddleware` using parsed allowed origins (from `.env`), defaulting to safe values, avoiding wildcard origins (`*`).
