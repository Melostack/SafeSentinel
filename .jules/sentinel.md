
## 2024-05-18 - [API Security Improvements]
**Vulnerability:** Found 3 security issues in `api/server.py`: 1) Overly permissive CORS `allow_origins=["*"]`. 2) Information leak via exception handler `detail=str(e)`. 3) Missing max length limits on Pydantic models.
**Learning:** Hardcoded wildcard CORS and raw exception string leaks are common pitfalls that can lead to cross-origin attacks and expose internal architecture. Unbounded string inputs in Pydantic models are a DoS risk.
**Prevention:** Always restrict CORS origins via environment variables, log full stack traces server-side and return generic error messages to clients, and implement max-length limits on all string inputs via `pydantic.Field`.
