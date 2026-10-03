## 2024-03-24 - Restrict CORS Configuration
**Vulnerability:** The CORS middleware was configured with `allow_origins=["*"]`, allowing any domain to access the API. This is a High Priority issue.
**Learning:** Overly permissive CORS allows malicious websites to make cross-origin requests to the API on behalf of authenticated users, which can lead to sensitive data exposure or unauthorized actions.
**Prevention:** Restrict allowed origins using environment variables (e.g., `FRONTEND_URL`) rather than wildcards, especially in production environments.
