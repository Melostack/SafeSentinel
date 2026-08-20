## 2024-08-20 - [Sentinel API Hardening]
**Vulnerability:** The API allowed wildcard CORS, lacked input bounds on Pydantic models (DoS risk), and leaked internal error stack traces to clients in exception handlers.
**Learning:** These three areas are common security oversights in rapid FastAPI development. Unbounded inputs can cause resource exhaustion, while wildcard CORS and raw exception leaks are severe security risks in production.
**Prevention:** Always restrict `allow_origins`, enforce field limits in Pydantic models using `Field(..., max_length=X)`, and handle generic exceptions by logging internally and returning sanitized HTTP error responses.
