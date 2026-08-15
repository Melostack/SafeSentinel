## 2024-05-24 - API Security Hardening (CORS, DoS, Info Leak)
**Vulnerability:** Overly permissive CORS (`*`), unbounded string inputs in Pydantic models leading to potential DoS, and raw exception string exposure.
**Learning:** Using `allow_origins=["*"]` allows any site to call the API. Missing length limits allows payload exhaustion. Exposing `str(e)` leaks internal stack details.
**Prevention:** Always restrict CORS using environment variables for allowed origins. Enforce strict `max_length` constraints on API models. Catch exceptions, log internally with `exc_info=True`, and return generic localized messages (e.g., "Erro interno do servidor").
