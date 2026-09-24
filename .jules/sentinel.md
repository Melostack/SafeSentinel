## 2026-09-24 - Exception Leakage and Permissive CORS
**Vulnerability:** The API exception handlers leaked exact error traces to the client and CORS `allow_origins` was set to `["*"]`.
**Learning:** Default FastAPI configurations and generic exception handlers often expose internal implementation details and bypass same-origin policies by default.
**Prevention:** Always restrict CORS to trusted domains and use logging modules to capture internal errors (`exc_info=True`) while returning generic error messages to unauthenticated clients.
