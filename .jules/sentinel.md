## 2024-05-24 - API Error Information Leakage
**Vulnerability:** Unhandled exceptions in the FastAPI server returned raw error strings (`str(e)`) to the client, potentially exposing sensitive stack traces and internal application state.
**Learning:** Returning raw exception messages in public endpoints is a critical information leakage risk that can reveal system details to attackers.
**Prevention:** Always catch top-level exceptions, log them securely internally using `exc_info=True`, and return generic, non-sensitive error messages to the client.
