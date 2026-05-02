## 2025-02-14 - Fix Information Leakage and API Vulnerabilities
**Vulnerability:** Fast API error handlers leaked stack traces, models allowed unbounded inputs leading to DoS, and CORS allowed all origins (`*`) which is permissive.
**Learning:** Hardcoded wildcard `allow_origins=["*"]` allows any site to make cross-origin requests; exceptions raised as HTTP 500 should never expose raw system traces (`detail=str(e)`).
**Prevention:** Always bound Pydantic models with `Field(..., max_length=X)`. Pass errors through `logging.error(e, exc_info=True)` for observability, but return static string details to users. Configure CORS dynamically from trusted environment sources (`FRONTEND_URL`).
