## 2024-05-18 - API Security Vulnerabilities
**Vulnerability:** Fast API implementation in `api/server.py` leaked information through unhandled stack traces, allowed arbitrary origins in CORS middleware, and lacked input limits on Pydantic models (DoS risk).
**Learning:** These three issues frequently surface in rapidly prototyped backend APIs without a secure-by-default architecture, highlighting the need to enforce standard boundaries in input parsing and error handling.
**Prevention:** Always restrict CORS origins using environment variables, sanitize exception details returned via the API (returning generic errors), and define explicit lengths on string inputs in request models.
