## 2024-05-18 - [API Security Improvements]
**Vulnerability:** Insecure CORS (`allow_origins=["*"]`), potential for Information Leakage via unhandled exceptions leaking raw error strings (`detail=str(e)`), and DoS risks due to missing payload bounds on Pydantic models.
**Learning:** Default unconstrained API configurations and lack of centralized error masking expose the system to cross-origin abuse, resource exhaustion, and potential architectural leaks.
**Prevention:** Always restrict CORS explicitly using environment variables for origin parsing. Always enforce length limits (`max_length`) in Pydantic schemas. Use generic messages for external 500 errors and employ localized logging with `exc_info=True` for debugging.
