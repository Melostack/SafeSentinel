## 2025-02-24 - [API Input Validation]
**Vulnerability:** Missing input length validation on API endpoints allow potential DoS via large payloads.
**Learning:** Pydantic models in FastAPI default to no length constraints on strings unless explicitly set with Field(max_length=...).
**Prevention:** Always use Field(..., max_length=N) for string inputs in Pydantic models exposed to the web.
