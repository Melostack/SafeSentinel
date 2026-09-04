## 2024-05-24 - [Overly Permissive CORS Configuration]
**Vulnerability:** CORS configured with allow_origins=["*"] in fastapi middleware
**Learning:** This exposes the application to attacks if sensitive operations are available or if cookie based auth is used
**Prevention:** Use a specific whitelist of allowed origins from environment variable

## 2024-05-24 - [Information Leakage and DoS Vulnerabilities]
**Vulnerability:** The application was leaking stack traces in error messages (`detail=str(e)`) and lacked string limits on input fields (`CheckRequest` and `IntentRequest`), making it vulnerable to DoS and information disclosure.
**Learning:** These vulnerabilities exist when developers prioritize debugging and rapid prototyping over secure error handling and input validation.
**Prevention:** Always log errors internally using `exc_info=True` and return generic error messages to the client. Enforce strict input validation, including length limits, on all user-provided data using mechanisms like Pydantic's `Field`.
