## 2024-05-24 - [CORS, Exception Leakage, and DoS Mitigation]
**Vulnerability:** Overly permissive CORS `allow_origins=["*"]`, potential DoS via unbounded string inputs in FastAPI/Pydantic models, and Information Leakage via returning `str(e)` in 500 errors.
**Learning:** Found multiple standard security vulnerabilities in `api/server.py`. The application accepted cross-origin requests from anywhere, lacked input length constraints, and directly exposed internal error messages.
**Prevention:** Always restrict CORS to trusted domains (e.g. via `FRONTEND_URL` env var), enforce strict `max_length` constraints on all Pydantic string fields, and log exceptions internally using `logging.error(..., exc_info=True)` while returning generic 500 status messages.
