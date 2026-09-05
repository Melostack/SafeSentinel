## 2024-05-30 - Fix FastAPI Security Vulnerabilities
**Vulnerability:** Fast API allowed all origins in CORS, didn't enforce string limits in Pydantic models (DoS risk), and leaked internal server error traces in the exception handler.
**Learning:** These defaults can leave the API vulnerable. Relying on default CORS configs and failing to validate data sizes are common pitfalls.
**Prevention:** Enforce string limits using Pydantic's `Field`, restrict CORS using env vars, and handle exceptions generically without leaking error details.
