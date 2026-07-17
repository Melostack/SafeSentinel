## 2024-05-15 - [API Security Improvements]
**Vulnerability:** Information leakage via stack trace, overly permissive CORS (`allow_origins=["*"]`), and missing input limits in Pydantic models.
**Learning:** Returning `str(e)` in exception handling leaks stack traces which can expose internal infrastructure details. Allowing all origins in CORS can lead to CSRF or data exfiltration. Missing input limits expose the app to DoS attacks.
**Prevention:** Always log exceptions securely (`exc_info=True`), return generic error messages, enforce restrictive CORS policies, and use `max_length` in Pydantic `Field` for all text inputs.
