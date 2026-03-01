## 2025-03-01 - [API Security Hardening]
**Vulnerability:** The API endpoints (`/check`, `/extract`) lacked authentication, were vulnerable to unbounded data (DoS) due to missing `max_length` in Pydantic models, and leaked internal errors to the client via raw exception strings.
**Learning:** Security controls like authentication, input validation, and secure error handling must be explicitly implemented in the API layer.
**Prevention:** Implement API key validation with constant-time comparison, enforce string length constraints in Pydantic models using `Field`, and catch internal exceptions to log them while returning generic error messages to clients.
