## 2024-05-20 - Fix Information Leakage and Add Input Validation in API
**Vulnerability:** Information Leakage via Error Details & Unbounded Data DoS. The API endpoints were returning raw error stacktraces in the HTTP response (`detail=str(e)`) and missing input length validation on Pydantic models.
**Learning:** Returning unhandled exception messages to the client exposes internal state and potentially sensitive information. Unbounded string fields in Pydantic models can lead to Denial of Service via large payloads.
**Prevention:** Always log exceptions internally using `logging.error(..., exc_info=True)` and return generic, non-sensitive messages to users. Define strict `max_length` attributes for all Pydantic string fields.
