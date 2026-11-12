## 2024-05-24 - [Overly Permissive CORS]
**Vulnerability:** The API allowed requests from any origin (`allow_origins=["*"]`), increasing the risk of CSRF or data exfiltration from malicious websites.
**Learning:** Defaulting to permissive CORS settings during development can easily leak into production. Always restrict origins to expected clients (like a configured frontend URL).
**Prevention:** Use an environment variable (like `FRONTEND_URL`) to dynamically configure the allowed origin, defaulting to local development addresses.
