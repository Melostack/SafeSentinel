## 2024-04-06 - [Fix Information Leakage and Missing Authentication in API]
**Vulnerability:** The `/check` and `/extract` endpoints were missing authentication and overly permissive CORS settings. The exception handlers were returning `str(e)` directly, exposing internal errors.
**Learning:** Returning unhandled exception details directly from a web server creates information leakage (CWE-209). APIs that allow unbounded public access via `allow_origins=["*"]` or without authentication keys are vulnerable to unverified use and possible abuse/quota exhaustion.
**Prevention:** Always implement `Depends` for authentication (e.g. `APIKeyHeader`), specifically configure CORS origins, and handle exceptions via proper internal logging, exposing generic safe messages to clients.
