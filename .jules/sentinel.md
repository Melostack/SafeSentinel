
## 2024-06-12 - [FastAPI Application Security Enhancements]
**Vulnerability:** Found multiple high and medium severity vulnerabilities in `api/server.py`: Overly permissive CORS (`allow_origins=["*"]`), unbounded Pydantic model inputs leading to DoS, and information leakage via `str(e)` in the global exception handler.
**Learning:** In FastAPI, it's a common oversight to leave default settings like permissive CORS during prototyping. Unbounded Pydantic models and default exception handling can silently become vectors for DoS and info leakage in production.
**Prevention:** Always restrict `allow_origins` using environment variables. Enforce `max_length` in all Pydantic string fields. Ensure generic error responses are returned to the client while internal logs capture full exceptions using `exc_info=True`.
