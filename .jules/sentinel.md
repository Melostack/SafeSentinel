## 2024-06-25 - [Multiple API Security Fixes]
**Vulnerability:** CORS wildcard `["*"]`, unbounded Pydantic model inputs (DoS risk), and exception handler leaking stack traces in `api/server.py`.
**Learning:** External-facing APIs can easily become vulnerable if inputs are unbound and errors expose backend internals. CORS configuration is often left open in dev and mistakenly pushed to prod.
**Prevention:** Use environment variables for CORS origins, enforce `max_length` using `pydantic.Field`, and always log exceptions internally while returning generic 500 errors to the client.
