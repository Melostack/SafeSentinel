## 2026-04-23 - Prevent Exposing Sensitive Details in Error Messages
**Vulnerability:** Exception handler in `api/server.py` exposed raw exception strings (`str(e)`) to end-users via HTTP 500 errors.
**Learning:** Returning `str(e)` directly in API responses can leak internal paths, stack traces, and sensitive internal errors to potential attackers.
**Prevention:** Always log full exceptions internally using `logger.error("...", exc_info=True)` and return a generic, non-sensitive error message (e.g., "An internal server error occurred") to clients.

## 2026-04-23 - Restrict Overly Permissive CORS Configurations
**Vulnerability:** The CORS configuration in `api/server.py` used `allow_origins=["*"]`, allowing requests from any domain.
**Learning:** Using `*` for allowed origins permits cross-site requests from untrusted malicious websites, defeating the purpose of CORS protection for web clients.
**Prevention:** Dynamically load allowed origins from a secure configuration (like the `FRONTEND_URL` environment variable) and default to restrictive options if unconfigured, rather than defaulting to wildcard permissions.
