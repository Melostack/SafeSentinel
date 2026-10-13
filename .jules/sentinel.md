## 2024-05-24 - Overly Permissive CORS Configuration
**Vulnerability:** The FastAPI application was configured with `allow_origins=["*"]`, allowing any domain to make cross-origin requests to the API. This is a significant security risk as it could lead to unauthorized data access or CSRF-like attacks if sensitive endpoints were added later or if internal APIs are exposed.
**Learning:** Defaulting to wildcard CORS is a common anti-pattern during rapid development that often leaks into production if not explicitly managed via environment variables.
**Prevention:** Always restrict CORS `allow_origins` to known, trusted domains using environment variables (e.g., `FRONTEND_URL`) parsed dynamically, defaulting to localhost for local development rather than wildcard `*`.
