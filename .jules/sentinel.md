## 2024-05-16 - Prevent information leakage and secure CORS configuration
**Vulnerability:** Fast API implementation exposed internal stack traces on 500 errors and allowed overly permissive `allow_origins=["*"]` in CORS settings.
**Learning:** Returning `str(e)` directly inside `HTTPException` creates information leakage which can expose sensitive logic or system structure. Permissive CORS (`["*"]`) can allow unauthorized origin access.
**Prevention:** Always log exceptions securely on the backend (`logging.error(..., exc_info=True)`) and return generalized error messages (`"An internal server error occurred."`) to the client. Limit CORS to specific verified domains (e.g., using a `FRONTEND_URL` environment variable).
