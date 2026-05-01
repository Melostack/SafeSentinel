
## 2026-05-01 - Fix Information Leakage and DoS Risk in API
**Vulnerability:** The API endpoint `/check` was returning raw internal exceptions to the user (`detail=str(e)`), risking sensitive information leakage. Additionally, the Pydantic models `CheckRequest` and `IntentRequest` had unbounded `str` fields, which could be exploited for resource exhaustion (DoS) by sending excessively large strings.
**Learning:** Returning `str(e)` from exception handlers directly to clients exposes internal state or dependencies. Pydantic models in FastAPI accept strings of unlimited length by default unless explicitly constrained with `Field(..., max_length=X)`.
**Prevention:** Always use `logging.error(..., exc_info=True)` for internal debugging and return generic messages like "Internal server error" to clients. Always use `Field` to bound text input lengths in Pydantic models.
