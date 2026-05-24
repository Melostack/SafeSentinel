## Sentinel's Journal

## 2024-05-24 - Fix CORS vulnerability and exception information leakage
**Vulnerability:** The application was using an overly permissive CORS configuration (`allow_origins=["*"]`) which could allow malicious websites to make cross-origin requests to the API. Additionally, the `/check` endpoint was leaking raw exception details (`str(e)`) in its 500 error responses, which could expose internal stack traces or sensitive environment information to an attacker. The API models `CheckRequest` and `IntentRequest` also lacked length limits on string fields, presenting a potential Denial of Service (DoS) vulnerability.
**Learning:** Overly permissive CORS and unhandled exception logging can expose sensitive information. Pydantic models need maximum length bounds to prevent large payload attacks.
**Prevention:** Always restrict CORS origins to trusted domains (e.g. via `FRONTEND_URL` environment variable). For exception handling, log the detailed error internally (`logging.error(e, exc_info=True)`) and return a generic, non-sensitive error message to the user. Always enforce length constraints on input strings using `Field(..., max_length=X)` in Pydantic models.
