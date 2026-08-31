## 2024-08-31 - FastAPI Security Misconfigurations
**Vulnerability:** Overly permissive CORS `allow_origins=["*"]`, missing input length limits on Pydantic models (DoS risk), and exception handlers leaking internal error details by returning `str(e)`.
**Learning:** Default FastAPI configurations can be insecure. Unrestricted CORS exposes APIs, missing input boundaries lead to DoS, and raw exceptions leak internal stack/details.
**Prevention:** Always restrict CORS to trusted domains via env variables. Enforce `max_length` using Pydantic `Field`. Log raw exceptions internally (`exc_info=True`) and return generic messages to clients.
