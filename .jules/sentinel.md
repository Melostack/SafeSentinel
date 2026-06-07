## 2024-11-20 - Fix Overly Permissive CORS Configuration
**Vulnerability:** The FastAPI server was configured with `allow_origins=["*"]`, allowing any origin to make cross-origin requests to the API. This exposes the API to Cross-Site Request Forgery (CSRF) and other attacks if it handles authenticated or sensitive requests.
**Learning:** Overly permissive CORS in a production-ready template is a common security gap that can be overlooked. Using environment variables correctly parsed for arrays is required to restrict allowed origins securely in FastAPI without hardcoding domains.
**Prevention:** Always restrict `allow_origins` to explicitly trusted domains (e.g., via a parsed `FRONTEND_URL` environment variable) instead of using the wildcard `*`.
